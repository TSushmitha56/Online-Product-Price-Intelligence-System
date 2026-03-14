# E-Commerce Platform Integration Strategy

This document outlines the technical feasibility, strategy, and legal considerations for extracting product and pricing data from five major e-commerce platforms: Amazon, eBay, Walmart, Target, and Best Buy.

---

## 1. Platform Comparison & Official API Research

| Platform | Official Public API | API Name | Free Tier | Auth Method | Rate Limits | Data Fields | Geo Limits |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Amazon** | Yes, Restricted | Product Advertising API (PA-API) | Yes (Performance Based) | Access/Secret Key (Affiliate account req.) | Initially 1 TPS / 8640 TPD | Price, Title, Image, URL, Reviews | Global (Region-locked keys) |
| **eBay** | Yes | eBay Browse API | Yes | OAuth 2.0 (Client Credentials) | 1,000 req/day (Free Tier) | Price, Title, Image, URL, Condition | Global |
| **Walmart** | Yes, Limited | Affiliate Marketing API | Yes (Affiliate approval req.) | Consumer ID + Private Key Signatures | 10 feeds/hour (mostly for publishing) | Price, Title, Description, Image | US-centric |
| **Target** | No (Publicly) | N/A | N/A | N/A | N/A | N/A | US-centric |
| **Best Buy**| Yes | Best Buy Developer API | Yes | API Key | 5 TPS / 50,000 TPD | Price, Title, Image, URL, SKU | US-centric |

### Key API Takeaways:
1. **Best Buy** and **eBay** are the most accessible, offering high rate limits and immediate developer access for fetching product details. These will be our primary initial integrations. 
2. **Amazon** requires generating active affiliate sales before maintaining PA-API access, introducing a "chicken-and-egg" barrier for a new project.
3. **Walmart** heavily restricts API data to protect against third-party repricers and requires approval. 
4. **Target** provides no official public product API without a formal partnership.

---

## 2. Web Scraping Feasibility (For Amazon, Target, Walmart)

Where APIs are restricted or nonexistent, scraping is the technical fallback.

| Platform | Difficulty | Anti-Bot Protections | Recommended Tools | Selectors (Conceptual) |
| :--- | :--- | :--- | :--- | :--- |
| **Amazon** | High | Aggressive IP blocking, CAPTCHA, dynamic DOM | Playwright + Residential Proxies | Title: `#productTitle`, Price: `.a-price-whole` |
| **Walmart**| High | PerimeterX (human verification), heavily dynamic React JS | Playwright / Selenium + Stealth Modes | Title: `[data-testid='product-title']` |
| **Target** | Medium | Akamai bot detection, dynamic JS hydration | Playwright + Request Interception | Title: `[data-test='product-title']` |

*Note: Pure `Requests + BeautifulSoup` is insufficient for these platforms due to dynamic JavaScript rendering and immediate header-based bot flagging. Headless browsers (like Playwright) configured with stealth plugins are mandatory.*

---

## 3. Integration Strategy

To manage the disparity between API and Scraped data sources, the system will utilize a **Unified Abstraction Layer**.

*   **Architecture**: A generic `BaseEcommerceClient` class that defines `search_product(keyword)` and `get_product_details(id)`.
*   **API Implementations**: `EbayClient` and `BestBuyClient` will inherit this base class and translate their respective JSON responses into our standard internal schema.
*   **Scraping Implementations**: `AmazonScraper` and `TargetScraper` will inherit the base class, initialize a headless browser, extract the HTML selectors, and return the identical standard internal schema.
*   **Update Frequency**: 
    * APIs (eBay/Best Buy): Queried in real-time on user demand.
    * Scrapers (Amazon/Target): Executed asynchronously via a queue (e.g., Celery) due to long spin-up times and high failure risk. Result cached heavily.
*   **Standard Schema Form**:
    ```json
    {
      "platform": "bestbuy",
      "product_id": "123456",
      "title": "Sony Headphones",
      "price": 299.99,
      "url": "https://...",
      "image_url": "https://..."
    }
    ```

---

## 4. API Credential Setup (eBay & Best Buy)

We have selected **eBay** and **Best Buy** for immediate API integration due to their free, accessible tiers.

### Step 1: eBay Setup
1. Register at `developer.ebay.com`.
2. Generate an "App ID" (Client ID) and "Cert ID" (Client Secret) for the Production environment.
3. OAuth 2.0 flow will be used backend-side to generate the application token.

### Step 2: Best Buy Setup
1. Register at `developer.bestbuy.com`.
2. Generate an API Key. 

### Step 3: Secure Storage
Credentials will be stored via `dotenv` and strictly excluded from version control.
```env
# .env file
EBAY_APP_ID=your_client_id_here
EBAY_CERT_ID=your_client_secret_here

BESTBUY_API_KEY=your_bestbuy_key_here
```

---

## 5. Legal & Ethical Considerations

1. **API Usage Compliance**: We must adhere to eBay and Best Buy's Developer Terms of Service, explicitly avoiding exceeding the 50,000 TPD (Best Buy) and 1,000 TPD (eBay) limits. 
2. **Scraping Legality**: Scraping public data is generally legal (e.g., *hiQ Labs v. LinkedIn*), but overriding technical barriers (CAPTCHAs) or ignoring explicit cease-and-desist warnings carries risk.
3. **Robots.txt & Politeness**: Scrapers must introduce random intervals (3-10 seconds) between requests to avoid stressing retailer servers. We will parse and respect the `robots.txt` disallow paths where feasible.
4. **Attribution**: Prices pulled via API (especially affiliate networks) usually require displaying the retailer's logo or a distinct "Buy on [Retailer]" affiliate link.

---

## 6. Fallback & Mitigation Strategy

E-commerce integrations are inherently brittle. The following failsafes will be implemented:

1. **API Quota Exceeded / 429 Errors**:
   Implement an exponential backoff retry mechanism (e.g., using Python's `tenacity` library). If the daily quota is entirely blown, the UI will degrade gracefully, displaying a "Prices Temporarily Unavailable" badge for that specific retailer while keeping others active.
2. **Scraping Blocked (CAPTCHA Trigger)**:
   If a Playwright instance hits a CAPTCHA, the scraping job must immediately abort to prevent permanent IP bans. The system will fall back to returning the last successfully cached price (stale data), flagging it in the UI with a "Last updated: X days ago" warning.
3. **DOM Changes**:
   Target HTML selectors change frequently. A unit-test suite mimicking the scraper must run nightly. If extraction fails, a Slack/Email alert is fired to the developer team to update the CSS selectors.
4. **Caching Layer**:
   All successful `get_product_details` calls (API or Scraped) will be cached in Redis with a 24-hour Time-To-Live (TTL). This drastically reduces downstream API requests and mitigates temporary downtime.
