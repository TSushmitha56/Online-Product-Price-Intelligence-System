from playwright.sync_api import sync_playwright
from scrapers.utils import get_random_headers, random_delay, get_browser_launch_kwargs

query = "mailbag"
url = f"https://www.amazon.com/s?k={query}&ref=nb_sb_noss"

with sync_playwright() as p:
    browser = p.chromium.launch(**get_browser_launch_kwargs())
    context = browser.new_context(
        user_agent=get_random_headers().get("User-Agent"),
        viewport={"width": 1366, "height": 768},
        java_script_enabled=True,
        locale="en-US"
    )
    context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    page = context.new_page()
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)  # Let JS render
    
    # Dump full HTML of first result card
    locator = page.locator("[data-component-type='s-search-result']")
    count = locator.count()
    print(f"Total results: {count}")

    for i in range(min(5, count)):
        card = locator.nth(i)
        print(f"\n--- Item {i} ---")
        print("Text:", card.text_content()[:300].replace('\n', ' '))
        
        # Try every possible price selector
        selectors_to_try = [
            ".a-price .a-offscreen",
            ".a-price-whole",
            ".a-color-price",
            ".a-price",
            "[data-a-color='price']",
            "span[class*='price']",
            ".s-price-instructions-style",
        ]
        for sel in selectors_to_try:
            loc = card.locator(sel)
            if loc.count() > 0:
                print(f"  {sel} ({loc.count()}): '{loc.first.text_content()[:80]}'")
    
    browser.close()
