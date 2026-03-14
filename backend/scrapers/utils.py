import os
import random
import time
import requests
import logging

logger = logging.getLogger(__name__)

# Static curated rotating User-Agent list (Desktop Chrome only)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

_CACHED_UA = random.choice(USER_AGENTS)

def get_random_headers(rotate=False) -> dict:
    """
    Generates realistic browser headers to evade basic bot detection.
    Caches UA per session, rotates if rotate=True.
    """
    global _CACHED_UA
    if rotate:
        new_ua = random.choice(USER_AGENTS)
        while new_ua == _CACHED_UA and len(USER_AGENTS) > 1:
            new_ua = random.choice(USER_AGENTS)
        _CACHED_UA = new_ua

    user_agent = _CACHED_UA

    # Base headers
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "sec-fetch-site": "none",
        "sec-fetch-mode": "navigate",
        "sec-fetch-dest": "document",
        "sec-fetch-user": "?1",
    }
    
    # Residential sec-ch headers mapped out (basic implementation)
    if "Chrome" in user_agent:
        headers["sec-ch-ua"] = '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"'
        headers["sec-ch-ua-mobile"] = "?1" if "Mobile" in user_agent else "?0"
        headers["sec-ch-ua-platform"] = '"Android"' if "Android" in user_agent else '"Windows"' if "Windows" in user_agent else '"macOS"'
        
    return headers

def get_stealth_args() -> list:
    """
    Arguments to pass to chromium to disable automation markers.
    """
    return ["--disable-blink-features=AutomationControlled"]

def is_headless() -> bool:
    """
    Checks environment for SCRAPER_HEADFUL override.
    """
    return os.environ.get("SCRAPER_HEADFUL", "false").lower() != "true"
    
def get_browser_launch_kwargs() -> dict:
    """
    Returns kwargs for browser.launch() combining stealth and headless states.
    """
    kwargs = {
        "headless": is_headless(),
        "args": get_stealth_args()
    }
    if not kwargs["headless"]:
        kwargs["args"].append("--start-maximized")
        kwargs["slow_mo"] = 120
    return kwargs

def random_delay(min_seconds: float = 2.0, max_seconds: float = 5.0):
    """
    Sleeps for a random duration to mimic human pacing.
    """
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def human_like_interaction(page):
    """
    Simulates human interactions like random mouse movements and scroll-triggered lazy loading.
    """
    random_delay(2, 4)
    # Slight mouse movement
    for _ in range(3):
        x = random.randint(100, 800)
        y = random.randint(100, 600)
        try:
            page.mouse.move(x, y)
        except Exception:
            pass
        random_delay(0.2, 0.5)
        
    # Scroll-triggered lazy loading (30%, 60%, 100%)
    try:
        height = page.evaluate("document.body.scrollHeight")
        page.evaluate(f"window.scrollTo(0, {height * 0.3})")
        random_delay(1.0, 1.5)
        
        page.evaluate(f"window.scrollTo(0, {height * 0.6})")
        random_delay(1.0, 1.5)
        
        page.evaluate(f"window.scrollTo(0, {height})")
        
        # Extended wait for lazy load items
        page.wait_for_timeout(2500)
    except Exception:
        pass
    random_delay(1, 2)

def check_captcha_and_selectors(page, context, platform: str, query: str, selectors: list[str], captcha_keywords: list[str], captcha_selectors: list[str] = None, use_timeout_fallback: bool = False):
    """
    Robust page load strategy. Wait for DOM, check for CAPTCHA text, and attempt to find valid selectors.
    Reloads once if items aren't found or if CAPTCHA detected (with a soft UA rotation).
    Returns a dict with locator, captcha_detected flag, and selector_used.
    """
    if captcha_selectors is None:
        captcha_selectors = []
        
    def _attempt_find():
        page.wait_for_load_state("domcontentloaded")
        human_like_interaction(page)
        
        # Detect CAPTCHA via keywords
        content = page.content().lower()
        if any(keyword.lower() in content for keyword in captcha_keywords):
            return {"status": "captcha"}
            
        # Detect CAPTCHA via selectors
        for cap_sel in captcha_selectors:
            if page.locator(cap_sel).count() > 0:
                return {"status": "captcha"}
                
        # Try multiple fallback selectors
        for sel in selectors:
            try:
                try:
                    page.wait_for_selector(sel, timeout=3000)
                except Exception:
                    if use_timeout_fallback:
                        page.wait_for_timeout(3000)
                    else:
                        continue
                        
                locator = page.locator(sel)
                if locator.count() > 0:
                    return {"status": "success", "locator": locator, "selector_used": sel}
            except Exception:
                continue
        return {"status": "not_found"}

    result = _attempt_find()
    captcha_detected = False
    
    if result["status"] == "captcha":
        captcha_detected = True
        logger.warning(f"SCRAPER_BLOCKED_PLATFORM={platform} SCRAPER_QUERY={query} (CAPTCHA threshold reached. Soft retrying with rotated headers..)")
        # Soft retry with new user-agent context
        new_headers = get_random_headers(rotate=True)
        context.set_extra_http_headers(new_headers)
        try:
            page.reload(wait_until="domcontentloaded", timeout=20000)
            result = _attempt_find()
            if result["status"] == "captcha":
                captcha_detected = True
            else:
                captcha_detected = False
        except Exception:
            pass

    if result["status"] == "not_found":
        logger.info(f"Retrying page load once for {platform} on query '{query}' (Empty DOM)")
        try:
            page.reload(wait_until="domcontentloaded", timeout=15000)
            result = _attempt_find()
        except Exception:
            pass

    if result.get("status") != "success":
        logger.warning(f"SCRAPER_BLOCKED_PLATFORM={platform} SCRAPER_QUERY={query} (Final Timeout/Selectors Not Found) captcha_detected={captcha_detected}")
        return {"locator": None, "captcha_detected": captcha_detected, "selector_used": None}
        
    return {"locator": result["locator"], "captcha_detected": captcha_detected, "selector_used": result["selector_used"]}

def retry_request(max_retries: int = 3, backoff_factor: float = 2.0):
    """
    A decorator to retry a function (like an HTTP fetch or DOM query) upon failure,
    using exponential backoff.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    logger.warning(f"Attempt {retries}/{max_retries} failed in {func.__name__}: {e}")
                    if retries == max_retries:
                        logger.error(f"Function {func.__name__} failed after {max_retries} retries.")
                        raise
                    sleep_time = backoff_factor ** retries
                    time.sleep(sleep_time)
        return wrapper
    return decorator
