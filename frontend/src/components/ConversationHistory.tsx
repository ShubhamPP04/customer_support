import React, { useEffect, useState } from 'react';
import { useChat } from '../context/ChatContext';
import { chatAPI, handleAPIError, convertAPIMessageToMessage } from '../services/api';
import { MessageSquare, Plus } from 'lucide-react';
import './ConversationHistory.css';

interface ConversationSummary {
  conversation_id: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

export const ConversationHistory: React.FC = () => {
  const { state, dispatch } = useChat();
  const [conversationSummaries, setConversationSummaries] = useState<ConversationSummary[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadConversations();
  }, []);

  // Auto-refresh conversations when refresh is triggered
  useEffect(() => {
    if (state.refreshTrigger > 0) {
      loadConversations();
    }
  }, [state.refreshTrigger]);

  const loadConversations = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await chatAPI.getAllConversations();
      setConversationSummaries(response.conversations);
    } catch (err) {
      setError(handleAPIError(err));
    } finally {
      setIsLoading(false);
    }
  };

  const loadConversationHistory = async (conversationId: string) => {
    try {
      const response = await chatAPI.getConversationHistory(conversationId);
      
      // Convert API messages to internal format
      const messages = response.messages.map((msg, index) => 
        convertAPIMessageToMessage(msg, index)
      );

      // Set the messages and current conversation
      dispatch({ type: 'SET_MESSAGES', payload: messages });
      dispatch({ type: 'SET_CURRENT_CONVERSATION', payload: conversationId });
      
    } catch (err) {
      setError(handleAPIError(err));
    }
  };

  const startNewConversation = () => {
    dispatch({ type: 'CLEAR_MESSAGES' });
    dispatch({ type: 'SET_CURRENT_CONVERSATION', payload: null });
  };

  const getConversationPreview = (conversationId: string): string => {
    const conversation = state.conversations.find(c => c.id === conversationId);
    if (conversation && conversation.messages.length > 0) {
      const firstUserMessage = conversation.messages.find(m => m.type === 'user');
      return firstUserMessage?.content.slice(0, 50) + '...' || 'New conversation';
    }
    return 'New conversation';
  };

  return (
    <div className="conversation-history">
      <div className="history-header">
        <div className="header-title">
          <MessageSquare size={18} />
          <span>Conversations</span>
        </div>
        <button 
          onClick={startNewConversation}
          className="new-conversation-btn"
          title="Start new conversation"
        >
          <Plus size={16} />
        </button>
      </div>

      {error && (
        <div className="history-error">
          <span>⚠️ {error}</span>
          <button onClick={loadConversations} className="retry-btn">
            Retry
          </button>
        </div>
      )}

      <div className="conversations-list">
        {isLoading ? (
          <div className="loading-state">
            <div className="loading-spinner"></div>
            <span>Loading conversations...</span>
          </div>
        ) : conversationSummaries.length === 0 ? (
          <div className="empty-conversations">
            <MessageSquare size={32} className="empty-icon" />
            <p>No conversations yet</p>
            <span>Start chatting to see your conversation history</span>
          </div>
        ) : (
          conversationSummaries.map((conv) => (
            <div
              key={conv.conversation_id}
              className={`conversation-item ${
                state.currentConversationId === conv.conversation_id ? 'active' : ''
              }`}
              onClick={() => loadConversationHistory(conv.conversation_id)}
            >
              <div className="conversation-main">
                <div className="conversation-preview">
                  {getConversationPreview(conv.conversation_id)}
                </div>
                <div className="conversation-meta">
                  <span className="message-count">
                    {conv.message_count} messages
                  </span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
