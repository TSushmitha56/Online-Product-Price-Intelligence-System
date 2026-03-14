"""
Amazon Product Scraper
======================

Uses Playwright (headless Chromium) to search Amazon's product listings.
Playwright is necessary because Amazon renders prices via JavaScript —
traditional HTTP requests with BeautifulSoup miss dynamically rendered elements.

Architecture:
    AmazonScraper.search_products(query)
        └── Playwright browser context (stealth mode)
              ├── Navigate to search URL
              ├── Scroll to trigger lazy-load
              ├── Dismiss region popup (if shown)
              ├── Detect CAPTCHA (abort if found)
              └── parse_product_card() × N results

Price Extraction Strategy (4-stage fallback):
    1. .a-price .a-offscreen   ← screen-reader text (most reliable)
    2. .a-price-whole + .a-price-fraction  ← split whole/cents display
    3. Regex scan of full card text  ← catches any $x.xx pattern
    4. aria-label attributes with $ values  ← accessibility labels

Anti-bot measures implemented:
    - Chromium launched in non-headless mode option (configurable)
    - navigator.webdriver flag overridden to appear as normal browser
    - Random user-agent from a pool of realistic browser strings
    - Random delay (1–3 seconds) before navigation
    - Viewport set to 1366×768 (common resolution)
    - Locale: en-US, timezone: America/New_York
    - @retry_request decorator: up to 3 retries with 2x exponential backoff

Limitations:
    - Amazon's CAPTCHA will block the scraper if IP is flagged
    - HTML structure changes may break selectors (update as needed)
    - Returns max 10 results per search to avoid detection
"""
