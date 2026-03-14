import os
import logging
from db.connection import init_db, SessionLocal, engine
from db.models import Product, Price
from db.crud import (
    create_product, get_product, update_product, delete_product,
    create_price, get_prices_by_product, latest_prices,
    create_search, get_user_search_history
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_tests():
    # 1. Initialize Tables
    logger.info("Initializing database tables...")
    init_db()
    
    db = SessionLocal()
    try:
        # 2. Insert Sample Products
        logger.info("Inserting products...")
        product1 = create_product(db, name="Sony WH-1000XM5", category="Electronics", image_url="http://example.com/sony.jpg")
        product2 = create_product(db, name="Apple AirPods Pro 2", category="Electronics", image_url="http://example.com/airpods.jpg")
        
        # Test deduping logic
        product1_dup = create_product(db, name="Sony WH-1000XM5", category="Electronics")
        assert product1.product_id == product1_dup.product_id, "Duplicate product creation failed"
        
        # 3. Insert Prices
        logger.info("Inserting prices...")
        create_price(db, product_id=product1.product_id, store_name="Amazon", price=348.00, product_url="http://amazon.com/sony")
        create_price(db, product_id=product1.product_id, store_name="Best Buy", price=349.99, product_url="http://bestbuy.com/sony")
        # Add a newer price for Amazon
        import time; time.sleep(0.1) # brief delay to ensure timestamp diff
        create_price(db, product_id=product1.product_id, store_name="Amazon", price=345.50, product_url="http://amazon.com/sony")
        
        create_price(db, product_id=product2.product_id, store_name="Walmart", price=239.00, product_url="http://walmart.com/airpods")
        
        # 4. Insert Search History
        logger.info("Inserting search history...")
        user1 = "user-123"
        create_search(db, user_id=user1, query="noise cancelling headphones")
        create_search(db, user_id=user1, query="Sony WH-1000XM5")
        
        # 5. Query and Verify
        logger.info("\n--- DB QUERY RESULTS ---")
        
        # Latest Prices Verification
        latest = latest_prices(db, product1.product_id)
        print(f"\nLatest Prices for '{product1.name}':")
        for p in latest:
            print(f" - {p.store_name}: ${p.price} ({p.timestamp})")
            
        # Foreign Key & Relations Verification
        retrieved_product = get_product(db, product1.product_id)
        print(f"\nProduct '{retrieved_product.name}' has {len(retrieved_product.prices)} total price records.")
            
        # Validation checks
        logger.info("\nChecking Validations (Expected to fail gracefully):")
        try:
            create_product(db, name="", category="Test")
            print("ERROR: Empty name validation failed to catch!")
        except Exception as e:
            print(f"Caught expected empty name error: {e}")
            
        try:
            create_price(db, product_id=product2.product_id, store_name="eBay", price=-10.00)
            print("ERROR: Negative price validation failed to catch!")
        except ValueError as e:
            print(f"Caught expected negative price error: {e}")
            
        try:
            create_price(db, product_id=product2.product_id, store_name="Target", price=10.00, product_url="not-a-url")
            print("ERROR: Invalid URL validation failed to catch!")
        except ValueError as e:
            print(f"Caught expected bad URL error: {e}")

        # Search History Verification
        history = get_user_search_history(db, user1)
        print(f"\nSearch History for {user1}:")
        for h in history:
            print(f" - {h.query} at {h.timestamp}")

        logger.info("\nAll database tests executed successfully!")

    finally:
        # Cleanup generated records for idempotency if needed, but for now we'll just close it.
        db.close()

if __name__ == "__main__":
    run_tests()
