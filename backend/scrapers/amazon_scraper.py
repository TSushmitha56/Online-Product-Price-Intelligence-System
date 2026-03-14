from typing import List, Optional
import logging
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright
from .base_scraper import BaseScraper, Product
from .utils import get_random_headers, random_delay, retry_request, get_browser_launch_kwargs, check_captcha_and_selectors

logger = logging.getLogger(__name__)

class AmazonScraper(BaseScraper):
    
    def __init__(self):
        # Force US Storefront suffix
        self.base_url = "https://www.amazon.com/s?k={query}&ref=nb_sb_noss"
        
    @retry_request(max_retries=3, backoff_factor=2)
    def handle_request(self, url: str):
        # We will wrap the Playwright script inside the search_products wrapper
        # rather than returning a static reference like BeautifulSoup
        pass

    def parse_product_card(self, element) -> Optional[Product]:
        import re
        try:
            asin = element.get_attribute("data-asin")
            if not asin:
                return None
                
            # Title
            title_loc = element.locator("h2 a span, h2 span")
            if title_loc.count() == 0:
                return None
            title = title_loc.first.inner_text().strip()
            if not title:
                return None
            
            # URL
            link_loc = element.locator("a.a-link-normal.s-no-outline, h2 a")
            url = ""
            if link_loc.count() > 0:
                href = link_loc.first.get_attribute("href")
                if href:
                    url = "https://www.amazon.com" + href if href.startswith("/") else href
            
            # Price — multi-strategy extraction
            price_val = None
            
            # Strategy 1: .a-offscreen (hidden but screen-reader accessible)
            price_loc = element.locator(".a-price .a-offscreen")
            if price_loc.count() > 0:
                for idx in range(price_loc.count()):
                    price_str = price_loc.nth(idx).text_content() or ""
                    clean = price_str.replace('$', '').replace(',', '').strip()
                    try:
                        v = float(clean)
                        if v > 0:
                            price_val = v
                            break
                    except ValueError:
                        pass
            
            # Strategy 2: Whole + fraction parts
            if price_val is None:
                whole_loc = element.locator(".a-price-whole")
                frac_loc = element.locator(".a-price-fraction")
                if whole_loc.count() > 0:
                    whole = whole_loc.first.text_content().replace(',', '').replace('.', '').strip()
                    frac = frac_loc.first.text_content().strip() if frac_loc.count() > 0 else "00"
                    try:
                        v = float(f"{whole}.{frac}")
                        if v > 0:
                            price_val = v
                    except ValueError:
                        pass

            # Strategy 3: Regex on the full text content of the card
            if price_val is None:
                full_text = element.text_content() or ""
                matches = re.findall(r'\$([\d,]+\.\d{2})', full_text)
                for m in matches:
                    try:
                        v = float(m.replace(',', ''))
                        if v > 0:
                            price_val = v
                            break
                    except ValueError:
                        pass

            # Strategy 4: aria-label on .a-color-price or similar spans
            if price_val is None:
                aria_locs = element.locator("[aria-label*='$']")
                if aria_locs.count() > 0:
                    for idx in range(aria_locs.count()):
                        label = aria_locs.nth(idx).get_attribute("aria-label") or ""
                        matches = re.findall(r'\$([\d,]+\.\d{2})', label)
                        for m in matches:
                            try:
                                v = float(m.replace(',', ''))
                                if v > 0:
                                    price_val = v
                                    break
                            except ValueError:
                                pass
                        if price_val:
                            break
                    
            # Image URL
            img_loc = element.locator("img.s-image")
            img_url = ""
            if img_loc.count() > 0:
                img_el = img_loc.first
                img_url = img_el.get_attribute("src") or img_el.get_attribute("data-src") or ""
                srcset = img_el.get_attribute("srcset")
                if srcset:
                    try:
                        urls = [p.strip().split(" ")[0] for p in srcset.split(",")]
                        if urls:
                            img_url = urls[-1]
                    except:
                        pass
                
            # Rating
            rating_loc = element.locator("i[data-cy='reviews-ratings-slot'] span.a-icon-alt, span[aria-label*='out of 5 stars']")
            rating_val = None
            if rating_loc.count() > 0:
                for idx in range(rating_loc.count()):
                    rating_str = rating_loc.nth(idx).text_content() or rating_loc.nth(idx).get_attribute("aria-label") or ""
                    if "out of 5 stars" in rating_str:
                        try:
                            rating_val = float(rating_str.split(" ")[0])
                            break
                        except ValueError:
                            pass
            
            # Also try reading the plain number shown next to stars (e.g. '4.0')
            if rating_val is None:
                plain_rating = element.locator(".a-size-small.a-color-base")
                if plain_rating.count() > 0:
                    try:
                        rating_val = float(plain_rating.first.text_content().strip())
                    except (ValueError, AttributeError):
                        pass
                        
            # Shipping
            shipping_loc = element.locator("span[aria-label*='shipping']")
            shipping = None
            if shipping_loc.count() > 0:
                try:
                    shipping = shipping_loc.first.get_attribute("aria-label").strip()
                except:
                    pass

            return {
                "platform": "amazon",
                "title": title,
                "price": price_val,
                "currency": "USD",
                "product_url": url,
                "image_url": img_url,
                "availability": "In Stock" if price_val else "Check on Amazon",
                "seller": "Amazon",
                "rating": rating_val,
                "shipping": shipping
            }
        except Exception as e:
            logger.warning(f"Error parsing an Amazon product card: {e}")
            return None

    def search_products(self, query: str) -> List[Product]:
        encoded_query = quote_plus(query)
        url = self.base_url.format(query=encoded_query)
        results = []
        
        logger.info(f"INFO SCRAPER_START platform=amazon query='{query}'")
        
        headers = get_random_headers()
        
        try:
            with sync_playwright() as p:
                launch_kwargs = get_browser_launch_kwargs()
                browser = p.chromium.launch(**launch_kwargs)
                
                # Set realistic viewport and user agent
                context = browser.new_context(
                    user_agent=headers.get("User-Agent"),
                    viewport={"width": 1366, "height": 768},
                    java_script_enabled=True,
                    locale="en-US",
                    timezone_id="America/New_York",
                    extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}
                )
                
                # Navigator override stealth inject
                context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                page = context.new_page()
                page.set_default_navigation_timeout(35000)
                page.set_default_timeout(12000)
                
                # Add human-like initial setup delay
                random_delay(1, 3)
                
                # Navigate and wait for network to settle so JS-rendered prices load
                try:
                    page.goto(url, wait_until="domcontentloaded")
                    page.wait_for_load_state("networkidle", timeout=8000)
                except Exception:
                    pass  # networkidle may timeout; proceed anyway
                
                # Scroll down to trigger lazy loading
                try:
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
                    page.wait_for_timeout(1500)
                    page.evaluate("window.scrollTo(0, 0)")
                    page.wait_for_timeout(500)
                except Exception:
                    pass
                
                # Handle Region Popup
                try:
                    # Amazon "Deliver to" popup
                    popup_loc = page.locator(".nav-global-location-data-modal-action, #nav-main-edge-node-modal")
                    if popup_loc.count() > 0:
                        close_btn = page.locator("[data-action='a-popover-close'], button[data-action='a-popover-close'], .a-button-close")
                        if close_btn.count() > 0:
                            close_btn.first.click()
                            random_delay(1, 2)
                except Exception:
                    pass
                
                # Wait for the search results container via robust util
                selectors = [
                    "[data-component-type='s-search-result']",
                    ".s-result-item",
                    "[data-asin]:not([data-asin=''])",
                    "div[data-index]"
                ]
                captcha_terms = [
                    "sorry, we just need to make sure you're not a robot", 
                    "type the characters you see",
                    "enter the characters"
                ]
                captcha_selectors = [
                    "form[action*='validateCaptcha']",
                    "#captchacharacters",
                    "iframe[src*='captcha']"
                ]
                
                result_dict = check_captcha_and_selectors(
                    page, context, "amazon", query, selectors, captcha_terms, captcha_selectors=captcha_selectors
                )
                
                locator = result_dict.get("locator")
                if not locator:
                    logger.info(f"INFO SCRAPER_SUCCESS parsed_items_count=0 dom_candidates_count=0 captcha_detected={result_dict.get('captcha_detected')} selector_used=None")
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
                
                logger.info(f"INFO SCRAPER_SUCCESS parsed_items_count={len(results)} dom_candidates_count={count} captcha_detected={result_dict.get('captcha_detected')} selector_used={result_dict.get('selector_used')}")
                browser.close()
                return results
                
        except Exception as e:
            logger.error(f"Amazon Scraper totally failed for query '{query}': {e}")
            return []
