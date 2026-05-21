"""End-to-end verification of the Mermaid badge + lightbox.

Material puts the rendered SVG inside a CLOSED shadow root attached
to <div class="mermaid">. Our JS:
  1. Wraps each .mermaid div + a badge in a sibling-based .rb-mermaid-wrap
  2. On click, MOVES the .mermaid div into the lightbox stage
  3. On close, moves it back into its placeholder

So the verification is:
  * After Material renders, .mermaid divs have non-zero size (shadow OK)
  * Each .mermaid is wrapped in .rb-mermaid-wrap with a badge sibling
  * Click badge → lightbox opens, .mermaid moves into stage,
    placeholder takes its place in the article
  * Wheel scroll transforms the moved .mermaid
  * Escape closes, moves diagram back
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/development/manipulation/architecture/"
SHOTS = Path("/tmp/rb-mermaid-screens")
SHOTS.mkdir(exist_ok=True)


def log(ok: bool, msg: str) -> None:
    print(f"  [{'OK  ' if ok else 'FAIL'}] {msg}")


def run() -> int:
    failures = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1400, "height": 900})
        page = ctx.new_page()
        page.on("console", lambda m: print(f"  [console.{m.type}] {m.text}") if "rb-mermaid" in m.text or m.type == "error" else None)
        page.on("pageerror", lambda e: print(f"  [PAGEERR] {e}"))

        print("\n=== 1. Load page ===")
        page.goto(URL, wait_until="networkidle", timeout=30_000)
        log(True, f"loaded {URL}")

        print("\n=== 2. Wait for Material's mermaid render (div has size) ===")
        try:
            page.wait_for_function(
                """() => {
                  const els = document.querySelectorAll('div.mermaid');
                  return els.length > 0 &&
                    Array.from(els).every(e => e.clientHeight > 0 || e.clientWidth > 0);
                }""",
                timeout=25_000,
            )
            sizes = page.evaluate(
                "Array.from(document.querySelectorAll('div.mermaid'))"
                ".map(e => ({w: e.clientWidth, h: e.clientHeight}))"
            )
            log(True, f"4 diagrams rendered: {sizes}")
        except Exception as e:
            failures += 1
            log(False, f"diagrams never got dimensions: {e}")
            sizes = page.evaluate(
                "Array.from(document.querySelectorAll('div.mermaid'))"
                ".map(e => ({w: e.clientWidth, h: e.clientHeight, html_len: e.innerHTML.length}))"
            )
            print(f"        sizes: {sizes}")

        print("\n=== 3. Each diagram is wrapped + has a badge sibling ===")
        wrap_info = page.evaluate(
            """() => Array.from(document.querySelectorAll('div.mermaid')).map(e => ({
              parent_is_wrap: e.parentElement && e.parentElement.classList.contains('rb-mermaid-wrap'),
              wrap_has_badge: !!(e.parentElement && e.parentElement.querySelector(':scope > .rb-zoom-badge')),
            }))"""
        )
        for i, info in enumerate(wrap_info):
            ok = info["parent_is_wrap"] and info["wrap_has_badge"]
            if not ok: failures += 1
            log(ok, f"diagram #{i}: wrapped={info['parent_is_wrap']} has_badge={info['wrap_has_badge']}")

        print("\n=== 4. Click first badge → lightbox opens ===")
        try:
            page.locator(".rb-zoom-badge").first.click(timeout=5_000)
            log(True, "click dispatched")
        except Exception as e:
            failures += 1
            log(False, f"badge click failed: {e}")
            browser.close()
            return failures

        try:
            page.wait_for_selector("#rb-mermaid-lightbox.rb-lb-open", timeout=2_000)
            log(True, "lightbox opened")
        except Exception as e:
            failures += 1
            log(False, f"lightbox did not open: {e}")

        # After requestAnimationFrame the initial fit-scale is applied.
        page.wait_for_timeout(200)
        state = page.evaluate(
            """() => {
              const ov = document.getElementById('rb-mermaid-lightbox');
              const stage = ov.querySelector('.rb-lb-stage');
              const moved = stage.querySelector('div.mermaid');
              const placeholder = document.querySelector('.rb-mermaid-placeholder');
              const r = moved ? moved.getBoundingClientRect() : null;
              return {
                open: ov.classList.contains('rb-lb-open'),
                display: getComputedStyle(ov).display,
                stage_has_mermaid_div: !!moved,
                // After transform: scale() the rendered (post-transform)
                // box is much larger than clientWidth/clientHeight.
                moved_rendered_size: r ? {w: Math.round(r.width), h: Math.round(r.height)} : null,
                moved_intrinsic: moved ? {w: moved.clientWidth, h: moved.clientHeight} : null,
                moved_transform: moved ? moved.style.transform : null,
                placeholder_exists: !!placeholder,
                article_no_longer_has_moved_div: document.querySelector('.md-content article div.mermaid') === null,
              };
            }"""
        )
        moved_w = state.get("moved_rendered_size", {}).get("w", 0) if state.get("moved_rendered_size") else 0
        moved_h = state.get("moved_rendered_size", {}).get("h", 0) if state.get("moved_rendered_size") else 0
        moved_has_size = moved_w > 200 and moved_h > 100  # rendered size after scale
        print(f"        {state}")
        for key in ("open", "stage_has_mermaid_div", "placeholder_exists"):
            ok = bool(state.get(key))
            if not ok: failures += 1
            log(ok, key)
        if not moved_has_size: failures += 1
        log(moved_has_size, f"moved_rendered_size={moved_w}x{moved_h} (>200x>100)")

        # Screenshot proof
        shot = SHOTS / "lightbox-open.png"
        page.screenshot(path=str(shot), full_page=False)
        log(True, f"screenshot → {shot}")

        print("\n=== 5. Wheel zoom transforms the moved diagram ===")
        pre = page.evaluate(
            "() => { var el = document.querySelector('#rb-mermaid-lightbox .rb-lb-stage div.mermaid');"
            "        return el ? el.style.transform : null; }"
        )
        page.evaluate(
            """() => {
              const ov = document.getElementById('rb-mermaid-lightbox');
              ov.dispatchEvent(new WheelEvent('wheel', { deltaY: -200, bubbles: true, cancelable: true }));
            }"""
        )
        # RAF-batched write — wait one animation frame for the transform
        # to be flushed to the DOM.
        page.wait_for_timeout(50)
        post = page.evaluate(
            "() => { var el = document.querySelector('#rb-mermaid-lightbox .rb-lb-stage div.mermaid');"
            "        return el ? el.style.transform : null; }"
        )
        ok = pre != post and post and "scale" in post
        if not ok: failures += 1
        log(ok, f"wheel transform: '{pre}' -> '{post}'")

        shot2 = SHOTS / "lightbox-zoomed.png"
        page.screenshot(path=str(shot2), full_page=False)
        log(True, f"zoomed screenshot → {shot2}")

        print("\n=== 6. Escape closes + diagram returns to article ===")
        page.keyboard.press("Escape")
        try:
            page.wait_for_function(
                """() => !document.querySelector('#rb-mermaid-lightbox.rb-lb-open') &&
                        document.querySelector('.md-content article div.mermaid') !== null &&
                        !document.querySelector('.rb-mermaid-placeholder')""",
                timeout=2_000,
            )
            log(True, "Escape closed + diagram restored in article")
        except Exception as e:
            failures += 1
            log(False, f"Escape did not restore: {e}")
            state2 = page.evaluate(
                """() => ({
                  lightbox_still_open: !!document.querySelector('#rb-mermaid-lightbox.rb-lb-open'),
                  diagram_back_in_article: !!document.querySelector('.md-content article div.mermaid'),
                  placeholder_still_present: !!document.querySelector('.rb-mermaid-placeholder'),
                })"""
            )
            print(f"        {state2}")

        browser.close()

    print(f"\n=== RESULT: {'PASS' if failures == 0 else 'FAIL'} ({failures} failure(s)) ===\n")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
