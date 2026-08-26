"""Split the MkDocs documentation into retrieval-sized chunks.

Usage (from the repository root):
    .venv/bin/python -m chatbot.chunker
"""

import random
import re
import urllib.parse
from collections.abc import Iterator
from dataclasses import dataclass, field, replace
from pathlib import Path

FRONT_MATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
FENCE = re.compile(r"^\s*(```|~~~)\s*([\w+-]*)")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*$")
HTML_TAG = re.compile(r"<[^>]+>")

MIN_CHARS_PER_CHUNK = 250    # below this, merge into the neighbouring section
MAX_CHARS_PER_CHUNK = 2000   # above this, split (~500 tokens)

# Mermaid blocks are diagram syntax, not prose. Only their labels are indexed.
MERMAID_KEYWORDS = {
    "graph", "flowchart", "sequencediagram", "classdiagram", "statediagram",
    "statediagram-v2", "erdiagram", "gantt", "pie", "journey",
    "td", "tb", "lr", "rl", "bt", "subgraph", "end", "participant",
    "class", "classdef", "style", "click", "linkstyle",
}
BRACKETED = re.compile(r'[\[\(\{]{1,2}\s*"?([^\[\]\(\)\{\}"|]+?)"?\s*[\]\)\}]{1,2}')
EDGE_LABEL = re.compile(r"\|\s*([^|]+?)\s*\|")            # A -->|label| B
SUBGRAPH = re.compile(r"^\s*subgraph\s+(.+)$", re.I)


@dataclass
class Section:
    """A heading and its body, before size normalisation."""

    title: str | None
    path: list[str]
    anchor: str | None
    body: str = ""
    part: int = 1
    n_parts: int = 1


@dataclass
class Chunk:
    """A retrieval unit. Only `text` is embedded; the rest is metadata."""

    text: str
    title: str | None
    heading_path: list[str] = field(default_factory=list)
    source: str = ""
    url: str = ""
    year: int | None = None
    part: int = 1
    n_parts: int = 1


def slugify(title: str) -> str:
    """Approximate the anchor MkDocs generates for a heading."""
    slug = title.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    return re.sub(r"[\s_]+", "-", slug.strip())


def has_prose(body: str, min_chars: int = 20) -> bool:
    """Whether real text remains once HTML tags and whitespace are removed.

    Drops layout-only sections (<hr />, <br />). Markdown images survive:
    their alt text is content.
    """
    cleaned = HTML_TAG.sub(" ", body)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return len(cleaned) >= min_chars


def strip_front_matter(text: str) -> tuple[str, dict[str, str]]:
    """Separate a leading YAML front matter block from the body."""
    match = FRONT_MATTER.match(text)
    if not match:
        return text, {}

    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()

    return text[match.end():], meta


def iter_lines(text: str) -> Iterator[tuple[str, str | None, str | None]]:
    """Yield (line, lang, fence) so callers can tell prose from code.

    `lang` is None outside fenced blocks, otherwise the opening fence's
    language. `fence` is "open", "close" or None. Without this, the 471
    comment lines starting with `#` inside code blocks read as headings.
    """
    lang: str | None = None
    for line in text.splitlines():
        match = FENCE.match(line)
        if match and lang is None:
            lang = (match.group(2) or "").lower()
            yield line, lang, "open"
        elif match:
            yield line, lang, "close"
            lang = None
        else:
            yield line, lang, None


def mermaid_to_text(block_lines: list[str]) -> list[str]:
    """Extract the readable labels from a mermaid block, dropping syntax."""
    labels: list[str] = []
    for line in block_lines:
        labels += [m.group(1) for m in BRACKETED.finditer(line)]
        labels += [m.group(1) for m in EDGE_LABEL.finditer(line)]
        subgraph = SUBGRAPH.match(line)
        if subgraph:
            labels.append(subgraph.group(1).strip().strip('"'))

    # Nodes repeat once per edge; deduplicate so frequency does not skew the
    # embedding towards whichever node has the most connections.
    seen: set[str] = set()
    unique: list[str] = []
    for label in labels:
        label = label.strip()
        if not label or label.lower() in MERMAID_KEYWORDS or label.lower() in seen:
            continue
        seen.add(label.lower())
        unique.append(label)
    return unique


def split_sections(text: str) -> list[Section]:
    """Split markdown at headings, tracking the heading hierarchy."""
    sections: list[Section] = []
    stack: list[str] = []
    current: Section | None = None
    lines: list[str] = []
    mermaid_buffer: list[str] | None = None

    def close_section() -> None:
        nonlocal lines
        if current is not None:
            current.body = "\n".join(lines).strip()
            if has_prose(current.body):
                sections.append(current)
        lines = []

    def open_section(title: str | None, path: list[str]) -> None:
        nonlocal current
        close_section()
        current = Section(
            title=title,
            path=list(path),
            anchor=slugify(title) if title else None,
        )

    for line, lang, fence in iter_lines(text):
        if lang == "mermaid":
            if fence == "open":
                mermaid_buffer = []
            elif fence == "close":
                labels = mermaid_to_text(mermaid_buffer or [])
                if labels:
                    if current is None:
                        open_section(None, [])
                    lines.append("Diagram: " + ", ".join(labels))
                mermaid_buffer = None
            elif mermaid_buffer is not None:
                mermaid_buffer.append(line)
            continue

        heading = HEADING.match(line) if lang is None else None
        if heading:
            level = len(heading.group(1))
            title = heading.group(2).strip()
            # Trim the stack to this heading's level, then push. A second H1
            # therefore restarts the hierarchy instead of nesting under the first.
            stack = stack[:level - 1]
            stack.append(title)
            open_section(title, stack)
        else:
            if current is None:
                open_section(None, [])
            lines.append(line)

    close_section()
    return sections


def common_prefix(a: list[str], b: list[str]) -> list[str]:
    """The hierarchy two sections share."""
    shared: list[str] = []
    for left, right in zip(a, b):
        if left != right:
            break
        shared.append(left)
    return shared


def merge_small(sections: list[Section]) -> list[Section]:
    """Absorb short sections into the next one, staying under the ceiling."""
    merged: list[Section] = []
    buffer: Section | None = None

    for section in sections:
        if buffer is None:
            buffer = replace(section)
            continue

        fits = len(buffer.body) + len(section.body) + 2 <= MAX_CHARS_PER_CHUNK
        if len(buffer.body) < MIN_CHARS_PER_CHUNK and fits:
            buffer.body = f"{buffer.body}\n\n{section.body}".strip()
            shared = common_prefix(buffer.path, section.path)
            # Once two topics are joined, the narrower title no longer describes
            # the content, so fall back to the shared parent.
            if shared != buffer.path:
                buffer.title = shared[-1] if shared else None
            buffer.path = shared
        else:
            merged.append(buffer)
            buffer = replace(section)

    if buffer is not None:
        merged.append(buffer)

    # The final section has no successor to merge forward into.
    if len(merged) >= 2 and len(merged[-1].body) < MIN_CHARS_PER_CHUNK:
        last = merged.pop()
        if len(merged[-1].body) + len(last.body) + 2 <= MAX_CHARS_PER_CHUNK:
            merged[-1].body += f"\n\n{last.body}"
            merged[-1].path = common_prefix(merged[-1].path, last.path)
        else:
            merged.append(last)
    return merged


def _atomic_units(body: str) -> list[str]:
    """Break a body into indivisible units: paragraphs and whole code blocks.

    A half-written shell command is worse than an oversized chunk, so fenced
    blocks are never split.
    """
    units: list[str] = []
    buffer: list[str] = []

    for line, lang, fence in iter_lines(body):
        if fence == "open":
            if buffer:
                units.append("\n".join(buffer))
                buffer = []
            buffer.append(line)
        elif fence == "close":
            buffer.append(line)
            units.append("\n".join(buffer))
            buffer = []
        elif lang is not None or line.strip():
            buffer.append(line)
        elif buffer:
            units.append("\n".join(buffer))
            buffer = []

    if buffer:
        units.append("\n".join(buffer))
    return units


def split_large(section: Section) -> list[Section]:
    """Split an oversized section into pieces, packing whole units only."""
    if len(section.body) <= MAX_CHARS_PER_CHUNK:
        return [replace(section)]

    pieces: list[str] = []
    current: list[str] = []
    for unit in _atomic_units(section.body):
        packed_len = sum(len(item) + 2 for item in current)
        if current and packed_len + len(unit) > MAX_CHARS_PER_CHUNK:
            pieces.append("\n\n".join(current))
            current = []
        current.append(unit)
    if current:
        pieces.append("\n\n".join(current))

    # Greedy packing leaves the remainder as the last piece. A 60-character
    # orphan is worth less than a slightly oversized neighbour.
    if len(pieces) >= 2 and len(pieces[-1]) < MIN_CHARS_PER_CHUNK:
        tail = pieces.pop()
        pieces[-1] = f"{pieces[-1]}\n\n{tail}"

    return [
        replace(section, body=piece, part=i, n_parts=len(pieces))
        for i, piece in enumerate(pieces, 1)
    ]


def to_url(path: Path, docs_root: Path, anchor: str | None) -> str:
    """Build the published URL for a section, quoting spaces in path names."""
    parts = list(path.relative_to(docs_root).with_suffix("").parts)
    if parts and parts[-1] == "index":
        parts = parts[:-1]        # index.md is served as its directory

    url = "/" + "/".join(urllib.parse.quote(part) for part in parts)
    if parts:
        url += "/"
    if anchor:
        url += f"#{anchor}"
    return url


def extract_year(rel_path: Path) -> int | None:
    """Read the year out of docs/years/<year>/..., used to demote old content."""
    parts = rel_path.parts
    if len(parts) >= 2 and parts[0] == "years":
        try:
            return int(parts[1])
        except ValueError:
            return None
    return None


def chunk_file(path: Path, docs_root: Path) -> list[Chunk]:
    """Turn one markdown file into chunks: split, then enforce min and max size."""
    text, _meta = strip_front_matter(path.read_text(encoding="utf-8"))
    rel = path.relative_to(docs_root)
    year = extract_year(rel)

    sized: list[Section] = []
    for section in merge_small(split_sections(text)):
        sized.extend(split_large(section))

    chunks: list[Chunk] = []
    for section in sized:
        # Applied after splitting so every part of a long section keeps its
        # hierarchy: "Setup" alone is ambiguous, "Manipulation > Setup" is not.
        breadcrumb = " > ".join(section.path)
        text_to_embed = f"{breadcrumb}\n\n{section.body}" if breadcrumb else section.body

        chunks.append(Chunk(
            text=text_to_embed,
            title=section.title,
            heading_path=section.path,
            source=str(rel),
            url=to_url(path, docs_root, section.anchor),
            year=year,
            part=section.part,
            n_parts=section.n_parts,
        ))

    return chunks


def main() -> None:
    docs_root = Path("docs")
    chunks = [c for md in sorted(docs_root.rglob("*.md")) for c in chunk_file(md, docs_root)]

    sizes = sorted(len(c.text) for c in chunks)
    oversized = sum(1 for c in chunks if len(c.text) > MAX_CHARS_PER_CHUNK)

    print(f"Total chunks: {len(chunks)}")
    print(f"Size  min {sizes[0]}  median {sizes[len(sizes) // 2]}  max {sizes[-1]}")
    print(f"Historical (dated): {sum(1 for c in chunks if c.year is not None)}")
    print(f"From split sections: {sum(1 for c in chunks if c.n_parts > 1)}")
    print(f"Over the ceiling: {oversized} (indivisible tables and code blocks)")
    print(f"With mermaid labels: {sum(1 for c in chunks if 'Diagram:' in c.text)}")

    print("\nLargest:")
    for chunk in sorted(chunks, key=lambda c: -len(c.text))[:3]:
        path = " > ".join(chunk.heading_path)[:50]
        print(f"  {len(chunk.text):>5}  {chunk.source}  {path}")

    print("\nSample:")
    for chunk in random.sample(chunks, 2):
        print(f"\n  {chunk.url}\n  {'-' * 60}")
        print("  " + chunk.text[:300].replace("\n", "\n  "))


if __name__ == "__main__":
    main()
