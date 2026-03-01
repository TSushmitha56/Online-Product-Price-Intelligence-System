import unittest
from comparison.matcher import normalize_name, is_match
from comparison.scorer import calculate_score, extract_shipping_cost
from comparison.aggregator import aggregate_prices

class TestPriceComparison(unittest.TestCase):

    def setUp(self):
        self.mock_product_1 = {
             "platform": "amazon",
             "title": "Sony WH-1000XM5 Wireless Headphones",
             "price": 348.00,
             "currency": "USD",
             "shipping": "Free shipping",
             "rating": 4.8,
             "product_url": "amazon.com/sony"
        }
        self.mock_product_2 = {
             "platform": "ebay",
             "title": "New Sony WH 1000XM5 Noise Cancelling",
             "price": 299.00,
             "currency": "USD",
             "shipping": "+$15.00 shipping",
             "rating": 3.9,
             "product_url": "ebay.com/sony"
        }
        self.mock_product_3 = {
             "platform": "walmart",
             "title": "Apple AirPods Pro 2",
             "price": 249.00,
             "currency": "USD",
             "shipping": "Free",
             "rating": 4.9,
             "product_url": "walmart.com/airpods"
        }

    def test_name_normalization_and_matching(self):
        query = "Sony WH-1000XM5"
        name1 = "Sony WH-1000XM5 Wireless Headphones"
        name2 = "New Sony WH 1000XM5 Noise Cancelling"
        name3 = "Apple AirPods Pro 2"
        
        norm_q = normalize_name(query)
        norm1 = normalize_name(name1)
        norm2 = normalize_name(name2)
        norm3 = normalize_name(name3)
        
        # We compare the search intent query with the title, which is how grouping functions
        self.assertTrue(is_match(norm_q, norm1, threshold=70.0))
        self.assertTrue(is_match(norm_q, norm2, threshold=70.0))
        self.assertFalse(is_match(norm_q, norm3, threshold=70.0))

    def test_shipping_extraction(self):
         self.assertEqual(extract_shipping_cost("Free shipping"), 0.0)
         self.assertEqual(extract_shipping_cost("+$15.99 shipping"), 15.99)
         self.assertEqual(extract_shipping_cost("No shipping info"), 0.0)

    def test_calculate_score(self):
         # Rating influence: same price & shipping, different rating
         score1 = calculate_score(100.0, 50.0, 150.0, 0.0, seller_rating=5.0) # norm_price: 0.5, norm_ship: 1.0, norm_rating: 1.0 => (0.6*0.5)+(0.2*1)+(0.2*1) = 0.3+0.2+0.2 = 0.7 => 70.0
         score2 = calculate_score(100.0, 50.0, 150.0, 0.0, seller_rating=2.5) # norm_price: 0.5, norm_ship: 1.0, norm_rating: 0.5 => (0.6*0.5)+(0.2*1)+(0.2*0.5) = 0.3+0.2+0.1 = 0.6 => 60.0
         self.assertTrue(score1 > score2)
         
         # Shipping difference
         score3 = calculate_score(100.0, 50.0, 150.0, 20.0, seller_rating=5.0) # shipping penalty
         self.assertTrue(score1 > score3)

    def test_aggregate_prices(self):
        query = "Sony WH-1000XM5"
        sources = [[self.mock_product_1, self.mock_product_2, self.mock_product_3]]
        
        result = aggregate_prices(query, sources, min_rating=3.0)
        
        # Validation
        self.assertEqual(result["query"], query)
        
        # The algorithm should have clustered only the 2 Sony products and discarded the Apple one.
        matched = result["matched_products"][0]
        self.assertEqual(matched["price_stats"]["count"], 2)
        self.assertEqual(matched["price_stats"]["lowest"], 299.00)
        self.assertEqual(matched["price_stats"]["highest"], 348.00)
        self.assertEqual(matched["price_stats"]["average"], 323.50)
        
        # The best offer logic: 
        # Amazon: price 348 (scale 0), shipping 0 (scale 1), rating 4.8 (scale 0.96) => 0 + 0.2 + ~0.19 = ~0.39 (39 score)
        # eBay: price 299 (scale 1), shipping 15 (scale 0.25), rating 3.9 (scale 0.78) => 0.6 + 0.05 + 0.15 = 0.8 (80 score)
        best_overall = matched["best_overall_offer"]
        self.assertEqual(best_overall["store"], "ebay")

if __name__ == '__main__':
    unittest.main()
