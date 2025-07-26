from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from models import get_database_url, Conversation, Message, get_session, create_database_engine
from chat_service import ChatService

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Flask-SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

db = SQLAlchemy()
db.init_app(app)

# Initialize chat service
chat_service = ChatService()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint
    Expected payload:
    {
        "message": "User's message",
        "conversation_id": "optional_conversation_id"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        user_message = data['message']
        conversation_id = data.get('conversation_id')
        
        # Get or create conversation
        engine = create_database_engine()
        session = get_session(engine)
        
        try:
            if conversation_id:
                conversation = session.query(Conversation).filter_by(session_id=conversation_id).first()
                if not conversation:
                    return jsonify({"error": "Conversation not found"}), 404
            else:
                # Create new conversation
                conversation_id = str(uuid.uuid4())
                conversation = Conversation(session_id=conversation_id)
                session.add(conversation)
                session.flush()  # Get the ID
            
            # Save user message
            user_msg = Message(
                conversation_id=conversation.id,
                message_type='user',
                content=user_message,
                timestamp=datetime.utcnow()
            )
            session.add(user_msg)
            
            # Generate AI response
            ai_response = chat_service.generate_response(user_message, conversation_id, session)
            
            # Save AI response
            ai_msg = Message(
                conversation_id=conversation.id,
                message_type='assistant',
                content=ai_response,
                timestamp=datetime.utcnow()
            )
            session.add(ai_msg)
            
            session.commit()
            
            return jsonify({
                "response": ai_response,
                "conversation_id": conversation.session_id,
                "timestamp": datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
    except Exception as e:
        app.logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/conversations/<conversation_id>/history', methods=['GET'])
def get_conversation_history(conversation_id):
    """Get conversation history"""
    try:
        engine = create_database_engine()
        session = get_session(engine)
        
        try:
            conversation = session.query(Conversation).filter_by(session_id=conversation_id).first()
            if not conversation:
                return jsonify({"error": "Conversation not found"}), 404
            
            messages = session.query(Message).filter_by(conversation_id=conversation.id).order_by(Message.timestamp).all()
            
            history = []
            for msg in messages:
                history.append({
                    "type": msg.message_type,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                })
            
            return jsonify({
                "conversation_id": conversation_id,
                "messages": history
            })
            
        finally:
            session.close()
            
    except Exception as e:
        app.logger.error(f"Error getting conversation history: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/conversations', methods=['GET'])
def list_conversations():
    """List all conversations (for admin/debugging)"""
    try:
        engine = create_database_engine()
        session = get_session(engine)
        
        try:
            conversations = session.query(Conversation).order_by(Conversation.created_at.desc()).limit(50).all()
            
            result = []
            for conv in conversations:
                message_count = session.query(Message).filter_by(conversation_id=conv.id).count()
                result.append({
                    "conversation_id": conv.session_id,
                    "created_at": conv.created_at.isoformat(),
                    "updated_at": conv.updated_at.isoformat(),
                    "message_count": message_count
                })
            
            return jsonify({"conversations": result})
            
        finally:
            session.close()
            
    except Exception as e:
        app.logger.error(f"Error listing conversations: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
