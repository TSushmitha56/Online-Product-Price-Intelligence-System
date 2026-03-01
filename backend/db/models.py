import uuid
from datetime import datetime
import re
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base, relationship, validates
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

# Utility to generate UUID string, compatible with SQlite fallback and Postgres String/UUID
def generate_uuid():
    return str(uuid.uuid4())

class Product(Base):
    __tablename__ = 'products'

    # we use String(36) to store UUIDs universally to accommodate SQLite fallbacks natively
    product_id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    category = Column(String, index=True)
    image_url = Column(String)

    # Relationships
    prices = relationship("Price", back_populates="product", cascade="all, delete-orphan")

    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Product name cannot be empty")
        return value.strip()


class Price(Base):
    __tablename__ = 'prices'

    price_id = Column(String(36), primary_key=True, default=generate_uuid)
    product_id = Column(String(36), ForeignKey('products.product_id'), index=True, nullable=False)
    store_name = Column(String, index=True, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    product_url = Column(String)

    # Relationships
    product = relationship("Product", back_populates="prices")

    @validates('price')
    def validate_price(self, key, value):
        val = float(value)
        if val <= 0:
            raise ValueError("Price must be greater than 0")
        return val

    @validates('product_url')
    def validate_url(self, key, value):
        if value:
            # Basic URL validation regex
            regex = re.compile(
                r'^(?:http|ftp)s?://' # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            if not re.match(regex, value):
                raise ValueError(f"Invalid URL format: {value}")
        return value


class SearchHistory(Base):
    __tablename__ = 'search_history'

    search_id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String, index=True, nullable=False)
    query = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    @validates('query')
    def validate_query(self, key, value):
        if not value or not value.strip():
            raise ValueError("Search query cannot be empty")
        return value.strip()
