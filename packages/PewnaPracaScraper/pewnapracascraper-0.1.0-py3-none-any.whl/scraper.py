# src/playwright_scraper/scraper.py
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError
import random
from typing import Tuple

# A short, refresh-able list is fine for most tasks.
USER_AGENTS: list[str] = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
]

def _random_ua() -> str:
    return random.choice(USER_AGENTS)


class ScrapeError(RuntimeError):
    """Raised when the page could not be downloaded."""


def scrape(url: str, *, timeout_ms: int = 15_000) -> str:
    """
    Fetch a page with Playwright and return its fully rendered HTML.

    Parameters
    ----------
    url : str
        Absolute or relative URL. If it does not start with http/https,
        'http://' is prefixed.
    timeout_ms : int, optional
        Playwright 'goto' timeout in milliseconds.

    Returns
    -------
    str
        HTML source **after** network idle.

    Raises
    ------
    ScrapeError
        For any error that occurs inside Playwright.
    """
    full_url = url if url.startswith(("http://", "https://")) else f"http://{url}"

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context(user_agent=_random_ua())
            page = context.new_page()
            page.goto(full_url, wait_until="networkidle", timeout=timeout_ms)
            html = page.content()
            browser.close()
            return html

    except PWTimeoutError as e:                       # fine-grained handling
        raise ScrapeError(f"Timed out after {timeout_ms} ms loading {full_url}") from e
    except Exception as e:                            # noqa: BLE001
        raise ScrapeError(str(e)) from e