from typing import List, Optional
import logging
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright
from .base_scraper import BaseScraper, Product
from .utils import get_random_headers, random_delay, retry_request, get_browser_launch_kwargs, check_captcha_and_selectors

logger = logging.getLogger(__name__)

class WalmartScraper(BaseScraper):
    
    def __init__(self):
        self.base_url = "https://www.walmart.com/search?q={query}"
        
    @retry_request(max_retries=3, backoff_factor=2)
    def handle_request(self, url: str):
        # We will wrap the Playwright script inside the search_products wrapper
        pass

    def parse_product_card(self, element) -> Optional[Product]:
        try:
            # element here is a Playwright Locator representing `[data-testid='item-stack'] div[role='group']`
            
            title_loc = element.locator("[data-automation-id='product-title']")
            if title_loc.count() == 0:
                return None
            title = title_loc.first.inner_text().strip()
            
            link_loc = element.locator("a")
            url = ""
            if link_loc.count() > 0:
                href = link_loc.first.get_attribute("href")
                if href:
                    if href.startswith("/"):
                        url = "https://www.walmart.com" + href
                    else:
                        url = href
            
            price_loc = element.locator("[data-automation-id='product-price'] span.w_iUH7")
            price_val = None
            if price_loc.count() > 0:
                price_str = price_loc.first.inner_text().strip().replace('$', '').replace(',', '')
                try:
                    price_val = float(price_str.split(' ')[0]) # Handle "$9.99 current price" text
                except ValueError:
                    pass
            
            img_loc = element.locator("img[data-testid='productTileImage']")
            img_url = ""
            if img_loc.count() > 0:
                img_el = img_loc.first
                img_url = img_el.get_attribute("src") or img_el.get_attribute("data-src") or ""
                
            brand_loc = element.locator("[data-automation-id='product-brand']")
            seller = ""
            if brand_loc.count() > 0:
                seller = brand_loc.first.inner_text().strip()
                
            rating_loc = element.locator("span.w_iUH7").filter(has_text="out of 5")
            rating_val = None
            if rating_loc.count() > 0:
                text = rating_loc.first.inner_text()
                try:
                    rating_val = float(text.split(" ")[0])
                except ValueError:
                    pass
            
            shipping_loc = element.locator("[data-automation-id='shipping-info']")
            shipping = ""
            if shipping_loc.count() > 0:
                shipping = shipping_loc.first.inner_text().strip()

            return {
                "platform": "walmart",
                "title": title,
                "price": price_val,
                "currency": "USD" if price_val is not None else "",
                "product_url": url,
                "image_url": img_url,
                "availability": "In Stock" if price_val else "Out of Stock/Unknown",
                "seller": seller,
                "rating": rating_val,
                "shipping": shipping
            }
        except Exception as e:
            logger.warning(f"Error parsing a Walmart product card: {e}")
            return None

    def search_products(self, query: str) -> List[Product]:
        encoded_query = quote_plus(query)
        url = self.base_url.format(query=encoded_query)
        results = []
        
        logger.info(f"INFO SCRAPER_START platform=walmart query='{query}'")
        
        headers = get_random_headers()
        
        try:
            with sync_playwright() as p:
                launch_kwargs = get_browser_launch_kwargs()
                browser = p.chromium.launch(**launch_kwargs)
                
                context = browser.new_context(
                    user_agent=headers.get("User-Agent"),
                    viewport={"width": 1366, "height": 768},
                    java_script_enabled=True,
                    locale="en-US",
                    timezone_id="America/New_York",
                    # Walmart's PerimeterX can sometimes be dodged with simple bypass headers
                    extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}
                )
                
                context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                page = context.new_page()
                
                page.set_default_navigation_timeout(30000)
                page.set_default_timeout(10000)
                
                random_delay(3, 6) # Walmart is aggressive, slightly longer delay
                
                # Navigate
                page.goto(url)
                
                selectors = ["[data-testid='item-stack'] > div[role='group']", "[data-item-id]"]
                captcha_terms = ["press and hold", "security check", "enter the characters"]
                captcha_selectors = ["iframe[src*='captcha']"]
                
                result_dict = check_captcha_and_selectors(
                    page, context, "walmart", query, selectors, captcha_terms, captcha_selectors=captcha_selectors, use_timeout_fallback=True
                )
                
                locator = result_dict.get("locator")
                if not locator:
                    logger.info(f"INFO SCRAPER_SUCCESS items=0 captcha_detected={result_dict.get('captcha_detected')} selector_used=None")
                    browser.close()
                    return []
                
                count = locator.count()
                
                for i in range(count):
                    if len(results) >= 10:
                        break
                        
                    card = locator.nth(i)
                    product = self.parse_product_card(card)
                    
                    if product:
                        results.append(product)
                
                logger.info(f"INFO SCRAPER_SUCCESS items={len(results)} captcha_detected={result_dict.get('captcha_detected')} selector_used={result_dict.get('selector_used')}")
                browser.close()
                return results
                
        except Exception as e:
            logger.error(f"Walmart Scraper totally failed for query '{query}': {e}")
            return []
