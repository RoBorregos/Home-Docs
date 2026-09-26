import argparse
import json
import os
import posixpath
import re
import sys
import urllib.request
from pathlib import Path

REPO = "RoBorregos/home2"
DOCS = Path(__file__).resolve().parent.parent / "docs"
DEV = DOCS / "development"

READMES = {
    "README.md": ("repo/home2.md", "home2"),
    "docker/README.md": ("integration/repo/docker.md", "Docker"),
    "vision/README.md": ("vision/repo/vision.md", "Vision"),
    "hri/README.md": ("HRI/repo/hri.md", "HRI"),
    "hri/microservices/stt/README.md": ("HRI/repo/stt.md", "Speech to Text"),
    "hri/proto_interfaces/README.md": ("HRI/repo/proto_interfaces.md", "Proto Interfaces"),
    "hri/packages/display/display/README.md": ("HRI/repo/display.md", "Display"),
    "manipulation/packages/pick_and_place/README.md": ("manipulation/repo/pick_and_place.md", "Pick and Place"),
    "manipulation/packages/vamp_moveit_plugin/ReadMe.md": ("manipulation/repo/vamp_moveit_plugin.md", "VAMP MoveIt Plugin"),
    "navigation/README.md": ("navigation/repo/navigation.md", "Navigation"),
}

LINK = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)((?:\s+\"[^\"]*\")?)\)")
FENCE = re.compile(r"^\s*(```|~~~)")


def fetch(url, accept=None):
    headers = {"User-Agent": "home-docs-sync"}
    if accept:
        headers["Accept"] = accept
    token = os.environ.get("GITHUB_TOKEN")
    if token and "api.github.com" in url:
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as resp:
        return resp.read().decode("utf-8")


def resolve_sha(ref):
    return fetch(f"https://api.github.com/repos/{REPO}/commits/{ref}", "application/vnd.github.sha").strip()


def last_change(src, sha):
    return json.loads(fetch(f"https://api.github.com/repos/{REPO}/commits?sha={sha}&path={src}&per_page=1"))[0]["sha"]


def rewrite_links(text, src, sha):
    base = posixpath.dirname(src)

    def repl(m):
        bang, label, target, title = m.groups()
        if re.match(r"^([a-z][a-z0-9+.-]*:|#)", target, re.I):
            return m.group(0)
        if bang:
            print(f"warning: relative image {target} in {src}", file=sys.stderr)
            return m.group(0)
        path, _, frag = target.partition("#")
        resolved = posixpath.normpath(path.lstrip("/") if path.startswith("/") else posixpath.join(base, path))
        url = f"https://github.com/{REPO}/blob/{sha}/{resolved}" + (f"#{frag}" if frag else "")
        return f"[{label}]({url}{title})"

    out, in_fence = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
        out.append(line if in_fence else LINK.sub(repl, line))
    return "\n".join(out)


def is_substantive(text):
    return any(line.strip() and not line.lstrip().startswith("#") for line in text.splitlines())


def render(src, title, text, sha):
    body = rewrite_links(text, src, sha).strip()
    lines = body.splitlines()
    if lines and lines[0].startswith("# "):
        heading, body = lines[0], "\n".join(lines[1:]).strip()
    else:
        heading = f"# {title}"
    source = f"https://github.com/{REPO}/blob/{sha}/{src}"
    return (
        f"---\ntitle: {json.dumps(title)}\n---\n\n{heading}\n\n"
        f'!!! info "Synced from home2"\n'
        f"    Generated from [`home2/{src}`]({source}) @ `{sha[:7]}` by `scripts/sync_home2_readmes.py`. "
        f"Edit the README in home2 instead of this page.\n\n{body}\n"
    )


def build(sha):
    files = {}
    for src, (target, title) in READMES.items():
        text = fetch(f"https://raw.githubusercontent.com/{REPO}/{sha}/{src}")
        if not is_substantive(text):
            print(f"skip {src}: no content beyond headings", file=sys.stderr)
            continue
        files[DEV / target] = render(src, title, text, last_change(src, sha))

    for folder in sorted({p.parent for p in files}):
        pages = sorted(p.name for p in files if p.parent == folder)
        files[folder / ".pages"] = "title: From home2 repo\nnav:\n" + "".join(f"    - {p}\n" for p in pages)
    return files


def managed_dirs():
    return {(DEV / target).parent for target, _ in READMES.values()}


def stale(files):
    return [p for d in managed_dirs() if d.is_dir() for p in d.glob("*.md") if p not in files]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ref", default="main")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--report")
    args = parser.parse_args()

    sha = resolve_sha(args.ref)
    files = build(sha)
    changed = [p for p, c in files.items() if not p.exists() or p.read_text() != c]
    removed = stale(files)

    lines = [("remove " if p in removed else "update ") + str(p.relative_to(DOCS.parent)) for p in changed + removed]
    for line in lines:
        print(line)
    if args.report:
        Path(args.report).write_text(
            f"Sync of READMEs from [{REPO}@{sha[:7]}](https://github.com/{REPO}/commit/{sha}).\n\n"
            + "".join(f"- `{line}`\n" for line in lines)
        )
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as out:
            out.write(f"sha={sha[:7]}\n")
    if args.check:
        sys.exit(1 if changed or removed else 0)

    for p in changed:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(files[p])
    for p in removed:
        p.unlink()
    print(f"home2 @ {sha}")


if __name__ == "__main__":
    main()
