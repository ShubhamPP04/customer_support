import os
import json
from groq import Groq
from sqlalchemy.orm import joinedload
from sqlalchemy import func, and_, desc
from models import Product, InventoryItem, Order, OrderItem, User
from dotenv import load_dotenv

load_dotenv()

class ChatService:
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        
    def generate_response(self, user_message, conversation_id, session):
        """Generate AI response using Groq LLM"""
        try:
            # Analyze the user's intent and extract relevant information
            intent_analysis = self._analyze_intent(user_message)
            
            # Based on intent, query the database for relevant information
            if intent_analysis['intent'] == 'top_products':
                return self._handle_top_products_query(intent_analysis, session)
            elif intent_analysis['intent'] == 'order_status':
                return self._handle_order_status_query(intent_analysis, session)
            elif intent_analysis['intent'] == 'stock_inquiry':
                return self._handle_stock_inquiry(intent_analysis, session)
            elif intent_analysis['intent'] == 'general_inquiry':
                return self._handle_general_inquiry(intent_analysis, session)
            else:
                return self._handle_clarification_request(user_message)
                
        except Exception as e:
            return f"I apologize, but I encountered an error while processing your request. Please try again or rephrase your question."
    
    def _analyze_intent(self, message):
        """Analyze user message to determine intent and extract entities"""
        prompt = f"""
        Analyze the following customer support message and determine the intent and extract relevant entities.
        
        Message: "{message}"
        
        Classify the intent as one of:
        - top_products: User asking about best-selling or most popular products
        - order_status: User asking about order status, tracking, or order details
        - stock_inquiry: User asking about product availability or inventory
        - general_inquiry: General questions about products, categories, etc.
        - unclear: Message is unclear or ambiguous
        
        Extract entities like:
        - order_id: Any order ID mentioned
        - product_name: Product name mentioned
        - quantity: Number of items requested
        - category: Product category
        - brand: Product brand
        
        Respond with only a JSON object in this format:
        {{
            "intent": "intent_name",
            "entities": {{
                "order_id": "extracted_order_id_or_null",
                "product_name": "extracted_product_name_or_null",
                "quantity": "extracted_quantity_or_null",
                "category": "extracted_category_or_null",
                "brand": "extracted_brand_or_null"
            }},
            "confidence": 0.95
        }}
        """
        
        try:
            response = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
                temperature=0.1,
                max_tokens=500
            )
            
            result = json.loads(response.choices[0].message.content.strip())
            return result
            
        except Exception as e:
            # Fallback to simple keyword matching
            message_lower = message.lower()
            if any(keyword in message_lower for keyword in ['top', 'best', 'most sold', 'popular', 'bestseller']):
                return {"intent": "top_products", "entities": {}, "confidence": 0.7}
            elif any(keyword in message_lower for keyword in ['order', 'status', 'tracking', 'shipped', 'delivered']):
                return {"intent": "order_status", "entities": {}, "confidence": 0.7}
            elif any(keyword in message_lower for keyword in ['stock', 'available', 'inventory', 'left', 'in stock']):
                return {"intent": "stock_inquiry", "entities": {}, "confidence": 0.7}
            else:
                return {"intent": "general_inquiry", "entities": {}, "confidence": 0.5}
    
    def _handle_top_products_query(self, intent_analysis, session):
        """Handle queries about top-selling products"""
        try:
            # Query for top 5 most sold products
            top_products = session.query(
                Product.name,
                Product.brand,
                Product.category,
                Product.retail_price,
                func.count(InventoryItem.id).label('sold_count')
            ).join(
                InventoryItem, Product.id == InventoryItem.product_id
            ).filter(
                InventoryItem.sold_at.isnot(None)
            ).group_by(
                Product.id, Product.name, Product.brand, Product.category, Product.retail_price
            ).order_by(
                desc('sold_count')
            ).limit(5).all()
            
            if not top_products:
                return "I couldn't find any sales data at the moment. Please try again later."
            
            response = "Here are the top 5 most sold products:\n\n"
            for i, product in enumerate(top_products, 1):
                response += f"{i}. **{product.name}** by {product.brand}\n"
                response += f"   - Category: {product.category}\n"
                response += f"   - Price: ${product.retail_price:.2f}\n"
                response += f"   - Units Sold: {product.sold_count}\n\n"
            
            return response
            
        except Exception as e:
            return "I encountered an issue retrieving the top products. Please try again."
    
    def _handle_order_status_query(self, intent_analysis, session):
        """Handle queries about order status"""
        entities = intent_analysis.get('entities', {})
        order_id = entities.get('order_id')
        
        if not order_id:
            return "To check your order status, please provide your order ID. For example: 'What's the status of order 12345?'"
        
        try:
            # Convert order_id to integer if possible
            try:
                order_id = int(order_id)
            except ValueError:
                return f"The order ID '{order_id}' doesn't appear to be valid. Please provide a numeric order ID."
            
            order = session.query(Order).filter_by(order_id=order_id).first()
            
            if not order:
                return f"I couldn't find an order with ID {order_id}. Please double-check the order ID and try again."
            
            # Get order items
            order_items = session.query(OrderItem).join(Product).filter_by(order_id=order_id).all()
            
            response = f"**Order #{order_id} Status:**\n\n"
            response += f"Status: {order.status}\n"
            response += f"Order Date: {order.created_at.strftime('%B %d, %Y') if order.created_at else 'N/A'}\n"
            
            if order.shipped_at:
                response += f"Shipped Date: {order.shipped_at.strftime('%B %d, %Y')}\n"
            if order.delivered_at:
                response += f"Delivered Date: {order.delivered_at.strftime('%B %d, %Y')}\n"
            
            response += f"Number of Items: {order.num_of_item}\n\n"
            
            if order_items:
                response += "**Items in this order:**\n"
                for item in order_items:
                    response += f"- {item.product.name} (Status: {item.status})\n"
            
            return response
            
        except Exception as e:
            return f"I encountered an issue checking the order status. Please try again."
    
    def _handle_stock_inquiry(self, intent_analysis, session):
        """Handle queries about product stock/inventory"""
        entities = intent_analysis.get('entities', {})
        product_name = entities.get('product_name')
        
        if not product_name:
            return "To check stock availability, please specify the product name. For example: 'How many Classic T-Shirts are left in stock?'"
        
        try:
            # Search for products by name (case-insensitive, partial match)
            products = session.query(Product).filter(
                Product.name.ilike(f'%{product_name}%')
            ).all()
            
            if not products:
                return f"I couldn't find any products matching '{product_name}'. Could you please check the spelling or try a different product name?"
            
            if len(products) > 5:
                return f"I found {len(products)} products matching '{product_name}'. Please be more specific with the product name."
            
            response = f"**Stock information for products matching '{product_name}':**\n\n"
            
            for product in products:
                # Count available inventory (not sold)
                available_stock = session.query(InventoryItem).filter(
                    and_(
                        InventoryItem.product_id == product.id,
                        InventoryItem.sold_at.is_(None)
                    )
                ).count()
                
                response += f"**{product.name}** by {product.brand}\n"
                response += f"- Available Stock: {available_stock} units\n"
                response += f"- Price: ${product.retail_price:.2f}\n"
                response += f"- Category: {product.category}\n\n"
            
            return response
            
        except Exception as e:
            return "I encountered an issue checking stock availability. Please try again."
    
    def _handle_general_inquiry(self, intent_analysis, session):
        """Handle general inquiries about products, categories, etc."""
        try:
            # Get some general statistics
            total_products = session.query(Product).count()
            categories = session.query(Product.category).distinct().limit(10).all()
            brands = session.query(Product.brand).distinct().limit(10).all()
            
            response = "**Welcome to our Customer Support!**\n\n"
            response += f"We have {total_products} products available in our store.\n\n"
            
            response += "**Popular Categories:**\n"
            for cat in categories[:5]:
                if cat[0]:
                    response += f"- {cat[0]}\n"
            
            response += "\n**Popular Brands:**\n"
            for brand in brands[:5]:
                if brand[0]:
                    response += f"- {brand[0]}\n"
            
            response += "\n**What can I help you with today?**\n"
            response += "- Check order status (provide order ID)\n"
            response += "- View top-selling products\n"
            response += "- Check product availability\n"
            response += "- Browse products by category or brand\n"
            
            return response
            
        except Exception as e:
            return "Hello! I'm here to help you with your shopping needs. You can ask me about order status, product availability, or our top-selling items."
    
    def _handle_clarification_request(self, message):
        """Handle unclear messages by asking clarifying questions"""
        return """I'd be happy to help! Could you please clarify what you're looking for? 

I can assist you with:
- **Order Status**: "What's the status of order 12345?"
- **Top Products**: "What are the most popular products?"
- **Stock Availability**: "How many Classic T-Shirts are in stock?"
- **General Information**: Ask about our products, categories, or brands

Please let me know how I can help you today!"""
