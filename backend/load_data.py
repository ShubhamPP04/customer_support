import pandas as pd
import os
from datetime import datetime
from models import (
    create_database_engine, create_tables, get_session,
    User, DistributionCenter, Product, InventoryItem, Order, OrderItem
)
from dotenv import load_dotenv

load_dotenv()

def parse_datetime(date_string):
    """Parse datetime string, handling None values"""
    if pd.isna(date_string) or date_string == '':
        return None
    try:
        return pd.to_datetime(date_string)
    except:
        return None

def load_distribution_centers(session, csv_path):
    """Load distribution centers data"""
    print("Loading distribution centers...")
    df = pd.read_csv(csv_path)
    
    for _, row in df.iterrows():
        center = DistributionCenter(
            id=row['id'],
            name=row['name'],
            latitude=row['latitude'],
            longitude=row['longitude']
        )
        session.merge(center)
    
    session.commit()
    print(f"Loaded {len(df)} distribution centers")

def load_users(session, csv_path):
    """Load users data"""
    print("Loading users...")
    df = pd.read_csv(csv_path)
    
    for _, row in df.iterrows():
        user = User(
            id=row['id'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            email=row['email'],
            age=row['age'] if not pd.isna(row['age']) else None,
            gender=row['gender'] if not pd.isna(row['gender']) else None,
            state=row['state'] if not pd.isna(row['state']) else None,
            street_address=row['street_address'] if not pd.isna(row['street_address']) else None,
            postal_code=row['postal_code'] if not pd.isna(row['postal_code']) else None,
            city=row['city'] if not pd.isna(row['city']) else None,
            country=row['country'] if not pd.isna(row['country']) else None,
            latitude=row['latitude'] if not pd.isna(row['latitude']) else None,
            longitude=row['longitude'] if not pd.isna(row['longitude']) else None,
            traffic_source=row['traffic_source'] if not pd.isna(row['traffic_source']) else None,
            created_at=parse_datetime(row['created_at'])
        )
        session.merge(user)
    
    session.commit()
    print(f"Loaded {len(df)} users")

def load_products(session, csv_path):
    """Load products data"""
    print("Loading products...")
    df = pd.read_csv(csv_path)
    
    for _, row in df.iterrows():
        product = Product(
            id=row['id'],
            cost=row['cost'] if not pd.isna(row['cost']) else None,
            category=row['category'] if not pd.isna(row['category']) else None,
            name=row['name'] if not pd.isna(row['name']) else None,
            brand=row['brand'] if not pd.isna(row['brand']) else None,
            retail_price=row['retail_price'] if not pd.isna(row['retail_price']) else None,
            department=row['department'] if not pd.isna(row['department']) else None,
            sku=row['sku'] if not pd.isna(row['sku']) else None,
            distribution_center_id=row['distribution_center_id'] if not pd.isna(row['distribution_center_id']) else None
        )
        session.merge(product)
    
    session.commit()
    print(f"Loaded {len(df)} products")

def load_inventory_items(session, csv_path):
    """Load inventory items data"""
    print("Loading inventory items...")
    df = pd.read_csv(csv_path)
    
    for _, row in df.iterrows():
        inventory_item = InventoryItem(
            id=row['id'],
            product_id=row['product_id'],
            created_at=parse_datetime(row['created_at']),
            sold_at=parse_datetime(row['sold_at']),
            cost=row['cost'] if not pd.isna(row['cost']) else None,
            product_category=row['product_category'] if not pd.isna(row['product_category']) else None,
            product_name=row['product_name'] if not pd.isna(row['product_name']) else None,
            product_brand=row['product_brand'] if not pd.isna(row['product_brand']) else None,
            product_retail_price=row['product_retail_price'] if not pd.isna(row['product_retail_price']) else None,
            product_department=row['product_department'] if not pd.isna(row['product_department']) else None,
            product_sku=row['product_sku'] if not pd.isna(row['product_sku']) else None,
            product_distribution_center_id=row['product_distribution_center_id'] if not pd.isna(row['product_distribution_center_id']) else None
        )
        session.merge(inventory_item)
    
    session.commit()
    print(f"Loaded {len(df)} inventory items")

def load_orders(session, csv_path):
    """Load orders data"""
    print("Loading orders...")
    df = pd.read_csv(csv_path)
    
    for _, row in df.iterrows():
        order = Order(
            order_id=row['order_id'],
            user_id=row['user_id'],
            status=row['status'] if not pd.isna(row['status']) else None,
            gender=row['gender'] if not pd.isna(row['gender']) else None,
            created_at=parse_datetime(row['created_at']),
            returned_at=parse_datetime(row['returned_at']),
            shipped_at=parse_datetime(row['shipped_at']),
            delivered_at=parse_datetime(row['delivered_at']),
            num_of_item=row['num_of_item'] if not pd.isna(row['num_of_item']) else None
        )
        session.merge(order)
    
    session.commit()
    print(f"Loaded {len(df)} orders")

def load_order_items(session, csv_path):
    """Load order items data"""
    print("Loading order items...")
    df = pd.read_csv(csv_path)
    
    for _, row in df.iterrows():
        order_item = OrderItem(
            id=row['id'],
            order_id=row['order_id'],
            user_id=row['user_id'],
            product_id=row['product_id'],
            inventory_item_id=row['inventory_item_id'],
            status=row['status'] if not pd.isna(row['status']) else None,
            created_at=parse_datetime(row['created_at']),
            shipped_at=parse_datetime(row['shipped_at']),
            delivered_at=parse_datetime(row['delivered_at']),
            returned_at=parse_datetime(row['returned_at'])
        )
        session.merge(order_item)
    
    session.commit()
    print(f"Loaded {len(df)} order items")

def main():
    """Main function to load all CSV data into the database"""
    # Create database engine and tables
    engine = create_database_engine()
    create_tables(engine)
    session = get_session(engine)
    
    # Define CSV file paths
    data_dir = "../archive"
    csv_files = {
        'distribution_centers': os.path.join(data_dir, 'distribution_centers.csv'),
        'users': os.path.join(data_dir, 'users.csv'),
        'products': os.path.join(data_dir, 'products.csv'),
        'inventory_items': os.path.join(data_dir, 'inventory_items.csv'),
        'orders': os.path.join(data_dir, 'orders.csv'),
        'order_items': os.path.join(data_dir, 'order_items.csv')
    }
    
    try:
        # Load data in correct order (respecting foreign key constraints)
        load_distribution_centers(session, csv_files['distribution_centers'])
        load_users(session, csv_files['users'])
        load_products(session, csv_files['products'])
        load_inventory_items(session, csv_files['inventory_items'])
        load_orders(session, csv_files['orders'])
        load_order_items(session, csv_files['order_items'])
        
        print("All data loaded successfully!")
        
    except Exception as e:
        print(f"Error loading data: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    main()
