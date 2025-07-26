import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), unique=True)
    age = Column(Integer)
    gender = Column(String(10))
    state = Column(String(100))
    street_address = Column(Text)
    postal_code = Column(String(20))
    city = Column(String(100))
    country = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    traffic_source = Column(String(100))
    created_at = Column(DateTime)

class DistributionCenter(Base):
    __tablename__ = 'distribution_centers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    cost = Column(Float)
    category = Column(String(100))
    name = Column(String(255))
    brand = Column(String(100))
    retail_price = Column(Float)
    department = Column(String(100))
    sku = Column(String(255))
    distribution_center_id = Column(Integer, ForeignKey('distribution_centers.id'))
    
    distribution_center = relationship("DistributionCenter")

class InventoryItem(Base):
    __tablename__ = 'inventory_items'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    created_at = Column(DateTime)
    sold_at = Column(DateTime, nullable=True)
    cost = Column(Float)
    product_category = Column(String(100))
    product_name = Column(String(255))
    product_brand = Column(String(100))
    product_retail_price = Column(Float)
    product_department = Column(String(100))
    product_sku = Column(String(255))
    product_distribution_center_id = Column(Integer)
    
    product = relationship("Product")

class Order(Base):
    __tablename__ = 'orders'
    
    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String(50))
    gender = Column(String(10))
    created_at = Column(DateTime)
    returned_at = Column(DateTime, nullable=True)
    shipped_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    num_of_item = Column(Integer)
    
    user = relationship("User")

class OrderItem(Base):
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    inventory_item_id = Column(Integer, ForeignKey('inventory_items.id'))
    status = Column(String(50))
    created_at = Column(DateTime)
    shipped_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    returned_at = Column(DateTime, nullable=True)
    
    order = relationship("Order")
    user = relationship("User")
    product = relationship("Product")
    inventory_item = relationship("InventoryItem")

# Conversation schema for chat functionality
class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)  # Allow anonymous users
    session_id = Column(String(255), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", backref="conversations")

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    message_type = Column(String(20))  # 'user' or 'assistant'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    conversation = relationship("Conversation", backref="messages")

def get_database_url():
    """Generate database URL from environment variables"""
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', 'password')
    db_name = os.getenv('DB_NAME', 'customer_support')
    
    return f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"

def create_database_engine():
    """Create and return database engine"""
    database_url = get_database_url()
    engine = create_engine(database_url, echo=True)
    return engine

def create_tables(engine):
    """Create all tables in the database"""
    Base.metadata.create_all(engine)

def get_session(engine):
    """Create and return database session"""
    Session = sessionmaker(bind=engine)
    return Session()
