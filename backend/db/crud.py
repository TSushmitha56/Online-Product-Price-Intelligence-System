from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from typing import List, Optional
from .models import Product, Price, SearchHistory

# --- Product CRUD ---

def create_product(db: Session, name: str, category: str, image_url: str = None) -> Product:
    # Check if a product with same name and category already exists to avoid duplicates
    existing_product = db.query(Product).filter(Product.name == name, Product.category == category).first()
    if existing_product:
        return existing_product
        
    db_product = Product(name=name, category=category, image_url=image_url)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: str) -> Optional[Product]:
    return db.query(Product).filter(Product.product_id == product_id).first()

def update_product(db: Session, product_id: str, **kwargs) -> Optional[Product]:
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    for key, value in kwargs.items():
        if hasattr(db_product, key):
            setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: str) -> bool:
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False

# --- Price CRUD ---

def create_price(db: Session, product_id: str, store_name: str, price: float, product_url: str = None) -> Price:
    db_price = Price(
        product_id=product_id,
        store_name=store_name,
        price=price,
        product_url=product_url
    )
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price

def get_prices_by_product(db: Session, product_id: str) -> List[Price]:
    return db.query(Price).filter(Price.product_id == product_id).order_by(desc(Price.timestamp)).all()

def latest_prices(db: Session, product_id: str) -> List[Price]:
    """
    Returns the most recent price for each store for a specific product.
    """
    # Simple approach: fetch all prices sorted by timestamp desc, then dedupe by store in python
    # (Cross-database compatible approach vs DISTINCT ON for postgres only)
    all_prices = db.query(Price).filter(Price.product_id == product_id).order_by(desc(Price.timestamp)).all()
    
    latest = {}
    for p in all_prices:
        if p.store_name not in latest:
            latest[p.store_name] = p
            
    return list(latest.values())

# --- Search History CRUD ---

def create_search(db: Session, user_id: str, query: str) -> SearchHistory:
    db_search = SearchHistory(user_id=user_id, query=query)
    db.add(db_search)
    db.commit()
    db.refresh(db_search)
    return db_search

def get_user_search_history(db: Session, user_id: str, limit: int = 10) -> List[SearchHistory]:
    return db.query(SearchHistory).filter(SearchHistory.user_id == user_id)\
             .order_by(desc(SearchHistory.timestamp)).limit(limit).all()
