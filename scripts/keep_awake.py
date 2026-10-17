"""Visit the Streamlit app with a real browser so Community Cloud does not put it to sleep.

Streamlit Community Cloud sleeps an app after a period without viewers. A plain HTTP request does
not count as a visit, so this script opens the app in headless Chromium, waits for it to render
and, if the app is already asleep, clicks the wake-up button.

On Community Cloud the app itself runs inside an iframe, so the Streamlit DOM is searched in every
frame of the page, not only the top-level document.
"""

import os
import sys
import time

from playwright.sync_api import sync_playwright

URL = os.environ.get("APP_URL", "https://bullets-over-hugs-xywe6yyf72amtjipl9zbwx.streamlit.app")
APP_SELECTOR = '[data-testid="stAppViewContainer"]'
WAKE_TEXTS = ("get this app back up", "wake up")
RENDER_TIMEOUT_S = 180


def find_in_frames(page, selector):
    """Return the first frame whose DOM contains `selector`, or None."""
    for frame in page.frames:
        try:
            if frame.locator(selector).count() > 0:
                return frame
        except Exception:
            continue
    return None


def click_wake_button(page) -> bool:
    for frame in page.frames:
        for text in WAKE_TEXTS:
            try:
                button = frame.get_by_role("button", name=text, exact=False)
                if button.count() > 0:
                    button.first.click(timeout=5_000)
                    return True
            except Exception:
                continue
    return False


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=90_000)
        page.wait_for_timeout(5_000)

        if click_wake_button(page):
            print("App was asleep: clicked the wake-up button, waiting for it to boot.")
            page.wait_for_timeout(60_000)
        else:
            print("No wake-up button: app is already running.")

        deadline = time.time() + RENDER_TIMEOUT_S
        frame = None
        while time.time() < deadline:
            frame = find_in_frames(page, APP_SELECTOR)
            if frame is not None:
                break
            page.wait_for_timeout(3_000)

        if frame is None:
            print(f"Streamlit app did not render within {RENDER_TIMEOUT_S}s. Title: {page.title()}", file=sys.stderr)
            browser.close()
            return 1

        # Keep the session open a moment so the visit is registered.
        page.wait_for_timeout(15_000)
        print(f"Streamlit app rendered (in frame {frame.url[:60]}...). Title: {page.title()}")
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
