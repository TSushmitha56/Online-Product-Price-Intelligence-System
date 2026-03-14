import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core.cache import cache
from db.models import Product, Price
from db.connection import SessionLocal
from unittest.mock import patch
import uuid

class APIEndpointsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.compare_url = reverse('compare_prices')
        self.history_url = reverse('price_history')
        # Clear cache before each test
        cache.clear()
        
        # Create a sample product and prices for history testing
        self.product_id = str(uuid.uuid4())
        self.session = SessionLocal()
        self.product = Product(
            product_id=self.product_id,
            name="Test Product",
            category="Test"
        )
        self.session.add(self.product)
        self.session.add(Price(
            product_id=self.product_id,
            store_name="Amazon",
            price=19.99
        ))
        self.session.add(Price(
            product_id=self.product_id,
            store_name="eBay",
            price=18.50
        ))
        self.session.commit()

    def tearDown(self):
        self.session.query(Price).filter(Price.product_id == self.product_id).delete()
        self.session.query(Product).filter(Product.product_id == self.product_id).delete()
        self.session.commit()
        self.session.close()

    def test_compare_prices_missing_product(self):
        """Test the compare-prices endpoint without the required 'product' parameter."""
        response = self.client.get(self.compare_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    @patch('api.views.search_all_platforms')
    @patch('api.views.aggregate_prices')
    def test_compare_prices_valid_request(self, mock_aggregate, mock_search):
        """Test normal execution of compare prices which misses cache and fetches new."""
        # Setup mocks
        mock_search.return_value = []
        mock_aggregate.return_value = {
            "matched_products": [{
                "best_overall_offer": {"store": "Amazon", "product_url": "http://amazon.com/test"},
                "offers": [
                    {"platform": "Amazon", "title": "Test", "price": 10.0, "currency": "USD", "product_url": "http://amazon.com/test"}
                ]
            }]
        }
        
        response = self.client.get(self.compare_url, {'product': 'Test Product'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check pagination schema
        self.assertIn('total_results', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['price'], 10.0)
        self.assertEqual(response.data['product_name'], "Test Product")

    @patch('api.views.search_all_platforms')
    def test_compare_prices_caching(self, mock_search):
        """Test that identical requests within the TTL retrieve from cache instead of scraping."""
        cache_key = "price_compare:Cached Product"
        cached_result = [{"platform": "Walmart", "title": "Cached", "price": 5.0, "currency": "USD", "product_url": "http://walmart.com"}]
        cache.set(cache_key, cached_result, timeout=600)
        
        response = self.client.get(self.compare_url, {'product': 'Cached Product'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], cached_result)
        # Verify scraping wasn't called
        mock_search.assert_not_called()

    def test_price_history_missing_id(self):
        """Test the price-history endpoint without the required 'product_id' parameter."""
        response = self.client.get(self.history_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_price_history_invalid_id(self):
        """Test the price-history endpoint with a non-existent UUID."""
        response = self.client.get(self.history_url, {'product_id': str(uuid.uuid4())})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_price_history_valid(self):
        """Test successful retrieval of price history."""
        response = self.client.get(self.history_url, {'product_id': self.product_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product_id'], self.product_id)
        self.assertEqual(len(response.data['history']), 2)
        # Assuming ascending chronological order as defined
        prices = [h['price'] for h in response.data['history']]
        self.assertTrue(19.99 in prices and 18.50 in prices)

    def test_throttling_rate_limit(self):
        """Verify the 20 requests per minute anonymous limit."""
        # Using the drf test client without credentials simulates Anon.
        url = f"{self.compare_url}?product=test"
        
        # We temporarily patch cache so we don't actually trigger searches 20 times.
        cache.set("price_compare:test", [])
        
        # Exhaust 20 requests
        for _ in range(20):
            res = self.client.get(url)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            
        # The 21st should be throttled
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
