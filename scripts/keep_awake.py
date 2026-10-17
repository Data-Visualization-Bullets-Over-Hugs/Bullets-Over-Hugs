"""Visit the Streamlit app with a real browser so Community Cloud does not put it to sleep.

Streamlit Community Cloud sleeps an app after a period without viewers. A plain HTTP request does
not count as a visit, so this script opens the app in headless Chromium, waits for it to render
and, if the app is already asleep, clicks the wake-up button.
"""

import os
import sys

from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import sync_playwright

URL = os.environ.get("APP_URL", "https://bullets-over-hugs-xywe6yyf72amtjipl9zbwx.streamlit.app")
WAKE_BUTTON = "text=/get this app back up/i"


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=90_000)

        # If the app is asleep, press the wake-up button and give it time to boot.
        try:
            page.locator(WAKE_BUTTON).first.click(timeout=10_000)
            print("App was asleep: clicked the wake-up button.")
            page.wait_for_timeout(60_000)
        except PlaywrightTimeout:
            print("No wake-up button: app is already running.")

        # Wait for Streamlit to render something and keep the session open a moment.
        try:
            page.wait_for_selector('[data-testid="stAppViewContainer"]', timeout=120_000)
            page.wait_for_timeout(15_000)
            print("Streamlit app rendered. Title:", page.title())
            status = 0
        except PlaywrightTimeout:
            print("Streamlit app did not render in time.", file=sys.stderr)
            status = 1
        browser.close()
    return status


if __name__ == "__main__":
    raise SystemExit(main())
