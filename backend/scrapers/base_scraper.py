from abc import ABC, abstractmethod
from typing import List, TypedDict, Optional

class Product(TypedDict):
    platform: str
    title: str
    price: Optional[float]
    currency: str
    product_url: str
    image_url: Optional[str]
    availability: Optional[str]
    seller: Optional[str]
    rating: Optional[float]
    shipping: Optional[str]

class BaseScraper(ABC):
    
    @abstractmethod
    def search_products(self, query: str) -> List[Product]:
        """
        Main entry point for fetching a list of products from a search query.
        """
        pass
        
    @abstractmethod
    def parse_product_card(self, element) -> Optional[Product]:
        """
        Parses a single product card element (e.g. BeautifulSoup Tag or Playwright Locator)
        and returns a Product dictionary.
        """
        pass
        
    @abstractmethod
    def handle_request(self, url: str):
        """
        Fetches the HTML or sets up the DOM for parsing.
        """
        pass
