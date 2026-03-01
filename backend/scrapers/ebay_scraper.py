from typing import List, Optional
import logging
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright
from .base_scraper import BaseScraper, Product
from .utils import get_random_headers, random_delay, retry_request, get_browser_launch_kwargs, check_captcha_and_selectors

logger = logging.getLogger(__name__)

class EbayScraper(BaseScraper):
    
    def __init__(self):
        self.base_url = "https://www.ebay.com/sch/i.html?_nkw={query}"
        
    @retry_request(max_retries=3, backoff_factor=2)
    def handle_request(self, url: str):
        pass

    def parse_product_card(self, element) -> Optional[Product]:
        try:
            # Title
            title_loc = element.locator('.s-item__title')
            if title_loc.count() == 0:
                return None
            title = title_loc.first.inner_text().strip()
            if title == "Shop on eBay":
                return None
            
            # Price
            price_loc = element.locator('.s-item__price')
            price_val = None
            if price_loc.count() > 0:
                price_str = price_loc.first.inner_text().strip()
                clean_str = price_str.split('to')[0].replace('$', '').replace(',', '').strip()
                try:
                    price_val = float(clean_str)
                except ValueError:
                    pass
                    
            # URL
            link_loc = element.locator('.s-item__link')
            url = ""
            if link_loc.count() > 0:
                href = link_loc.first.get_attribute('href')
                if href:
                    url = href.split('?')[0]
                
            # Image URL
            img_loc = element.locator('.s-item__image-img')
            img_url = ""
            if img_loc.count() > 0:
                img_el = img_loc.first
                img_url = img_el.get_attribute('src') or img_el.get_attribute('data-src') or ""
                
                # ebay often puts a generic 1x1 gif in src if lazy load hasn't finished
                if "s-l500.gif" in img_url or "s-l140.gif" in img_url or "s-l400.gif" in img_url or img_url.startswith("data:image") or "1x1" in img_url:
                    img_url = img_el.get_attribute('data-src') or img_el.get_attribute('data-image-src') or img_url
            
            # Shipping
            shipping_loc = element.locator('.s-item__logisticsCost')
            shipping = ""
            if shipping_loc.count() > 0:
                shipping = shipping_loc.first.inner_text().strip()
            
            # Seller
            seller_loc = element.locator('.s-item__seller-info-text')
            seller = ""
            if seller_loc.count() > 0:
                seller = seller_loc.first.inner_text().strip()

            rating_loc = element.locator('.x-star-rating .clipped')
            rating_val = None
            if rating_loc.count() > 0:
                rating_str = rating_loc.first.inner_text().split(' ')[0]
                try:
                    rating_val = float(rating_str)
                except ValueError:
                    pass

            return {
                "platform": "ebay",
                "title": title,
                "price": price_val,
                "currency": "USD" if price_val is not None else "",
                "product_url": url,
                "image_url": img_url,
                "availability": "In Stock", # eBay listings implies stock
                "seller": seller,
                "rating": rating_val,
                "shipping": shipping
            }
        except Exception as e:
            logger.warning(f"Error parsing an eBay product card: {e}")
            return None

    def search_products(self, query: str) -> List[Product]:
        encoded_query = quote_plus(query)
        url = self.base_url.format(query=encoded_query)
        results = []
        
        logger.info(f"INFO SCRAPER_START platform=ebay query='{query}'")
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
                    extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}
                )
                
                context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                page = context.new_page()
                page.set_default_navigation_timeout(30000)
                page.set_default_timeout(10000)
                
                random_delay(2, 5)
                page.goto(url)
                
                selectors = [".s-item", ".srp-results li"]
                captcha_terms = ["please verify you are a human", "security measure", "enter the characters"]
                captcha_selectors = ["iframe[src*='captcha']"]
                
                result_dict = check_captcha_and_selectors(
                    page, context, "ebay", query, selectors, captcha_terms, captcha_selectors=captcha_selectors, use_timeout_fallback=True
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
            logger.error(f"eBay Scraper totally failed for query '{query}': {e}")
            return []
