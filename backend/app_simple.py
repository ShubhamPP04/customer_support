from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Simple in-memory storage for demo (replace with database later)
conversations = {}
messages = {}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint - simplified version for testing
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        user_message = data['message']
        conversation_id = data.get('conversation_id') or str(uuid.uuid4())
        
        # Simple responses for testing
        if 'top' in user_message.lower() and 'product' in user_message.lower():
            ai_response = """Here are the top 5 most sold products:

1. **Low Profile Dyed Cotton Twill Cap - Navy** by MG
   - Category: Accessories
   - Price: $6.25
   - Units Sold: 45

2. **Classic T-Shirt - Black** by Basic Wear
   - Category: Tops
   - Price: $19.99
   - Units Sold: 38

3. **Denim Jeans - Blue** by TrendyFit
   - Category: Bottoms
   - Price: $49.99
   - Units Sold: 32

4. **Enzyme Regular Solid Army Caps-Black** by MG
   - Category: Accessories
   - Price: $10.99
   - Units Sold: 28

5. **Basic Hoodie - Gray** by Comfort Zone
   - Category: Outerwear
   - Price: $34.99
   - Units Sold: 25"""
        
        elif 'order' in user_message.lower() and any(char.isdigit() for char in user_message):
            # Extract order ID
            order_id = ''.join(filter(str.isdigit, user_message))
            ai_response = f"""**Order #{order_id} Status:**

Status: Shipped
Order Date: July 20, 2025
Shipped Date: July 22, 2025
Number of Items: 2

**Items in this order:**
- Classic T-Shirt - Black (Status: Shipped)
- Low Profile Cap - Navy (Status: Shipped)

Your order is on its way and should arrive within 2-3 business days!"""
        
        elif 'stock' in user_message.lower() or 'inventory' in user_message.lower():
            ai_response = """**Stock Information:**

**Classic T-Shirts** - Available Stock: 127 units
- Price: $19.99
- Category: Tops

**T-Shirt Variants:**
- Black: 45 units
- White: 38 units
- Navy: 32 units
- Gray: 12 units

All variants are currently in stock and ready to ship!"""
        
        else:
            ai_response = """Hello! I'm your Customer Support Assistant. I can help you with:

• **Order Status**: "What's the status of order 12345?"
• **Top Products**: "What are the most popular products?"
• **Stock Availability**: "How many Classic T-Shirts are in stock?"
• **General Information**: Ask about our products, categories, or brands

What would you like to know today?"""
        
        # Store the conversation (in-memory for demo)
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        conversations[conversation_id].append({
            'type': 'user',
            'content': user_message,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        conversations[conversation_id].append({
            'type': 'assistant', 
            'content': ai_response,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        return jsonify({
            "response": ai_response,
            "conversation_id": conversation_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        app.logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/conversations/<conversation_id>/history', methods=['GET'])
def get_conversation_history(conversation_id):
    """Get conversation history"""
    try:
        if conversation_id not in conversations:
            return jsonify({"error": "Conversation not found"}), 404
        
        return jsonify({
            "conversation_id": conversation_id,
            "messages": conversations[conversation_id]
        })
        
    except Exception as e:
        app.logger.error(f"Error getting conversation history: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/conversations', methods=['GET'])
def list_conversations():
    """List all conversations"""
    try:
        result = []
        for conv_id, messages in conversations.items():
            if messages:
                result.append({
                    "conversation_id": conv_id,
                    "created_at": messages[0]['timestamp'],
                    "updated_at": messages[-1]['timestamp'],
                    "message_count": len(messages)
                })
        
        # Sort by updated_at descending
        result.sort(key=lambda x: x['updated_at'], reverse=True)
        
        return jsonify({"conversations": result})
        
    except Exception as e:
        app.logger.error(f"Error listing conversations: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
