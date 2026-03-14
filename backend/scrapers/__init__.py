from .base_scraper import Product
from .amazon_scraper import AmazonScraper
from .ebay_scraper import EbayScraper
from .walmart_scraper import WalmartScraper

import logging

logger = logging.getLogger(__name__)

def search_all_platforms(query: str) -> list[Product]:
    """
    Given a query, spins up all defined scrapers, merges their results,
    normalizes the schema, and returns the aggregated list of Products.
    """
    scrapers = [
        EbayScraper(),
        AmazonScraper(),
        WalmartScraper()
    ]
    
    all_results = []
    
    for scraper in scrapers:
        try:
            results = scraper.search_products(query)
            all_results.extend(results)
        except Exception as e:
            logger.error(f"Failed to scrape {scraper.__class__.__name__}: {e}")
            
    return all_results
