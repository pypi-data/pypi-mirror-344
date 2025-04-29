# PewnaPraca Scraper

*A tiny helper that returns fully-rendered HTML using [Microsoft Playwright](https://playwright.dev/python/).*

## ✨ Features

- **Headless Chromium** out-of-the-box  
- Rotates a short list of desktop **user-agents**  
- Single public API: `scrape(url, timeout_ms=15_000)`  
- Pure Python, no Flask/Django coupling  
- MIT-licensed & type-hinted

## 📦 Installation

```bash
pip install -U playwright-scraper            # package
playwright install chromium                  # one-time browser download