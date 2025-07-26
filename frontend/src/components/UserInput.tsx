import React, { useState, KeyboardEvent } from 'react';
import { useChat } from '../context/ChatContext';
import { chatAPI, handleAPIError } from '../services/api';
import { Send, Loader2 } from 'lucide-react';
import { v4 as uuidv4 } from 'uuid';
import './UserInput.css';

export const UserInput: React.FC = () => {
  const { state, dispatch } = useChat();
  const [localError, setLocalError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await sendMessage();
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const sendMessage = async () => {
    const message = state.inputValue.trim();
    if (!message || state.isLoading) return;

    // Clear any previous errors
    setLocalError(null);
    dispatch({ type: 'SET_ERROR', payload: null });

    // Add user message to the chat
    const userMessage = {
      id: uuidv4(),
      type: 'user' as const,
      content: message,
      timestamp: new Date().toISOString(),
    };

    dispatch({ type: 'ADD_MESSAGE', payload: userMessage });
    dispatch({ type: 'SET_INPUT_VALUE', payload: '' });
    dispatch({ type: 'SET_LOADING', payload: true });

    try {
      // Send message to backend
      const response = await chatAPI.sendMessage(message, state.currentConversationId || undefined);

      // Add AI response to the chat
      const aiMessage = {
        id: uuidv4(),
        type: 'assistant' as const,
        content: response.response,
        timestamp: response.timestamp,
      };

      dispatch({ type: 'ADD_MESSAGE', payload: aiMessage });

      // Update current conversation ID if it's a new conversation
      if (!state.currentConversationId) {
        dispatch({ type: 'SET_CURRENT_CONVERSATION', payload: response.conversation_id });
      }

      // Update conversation in the list
      const updatedMessages = [...state.messages, userMessage, aiMessage];
      dispatch({ 
        type: 'UPDATE_CONVERSATION', 
        payload: { 
          id: response.conversation_id, 
          messages: updatedMessages 
        } 
      });

      // Add new conversation if it doesn't exist
      if (!state.currentConversationId) {
        const newConversation = {
          id: response.conversation_id,
          messages: updatedMessages,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString()
        };
        dispatch({ type: 'ADD_CONVERSATION', payload: newConversation });
      }

    } catch (error) {
      const errorMessage = handleAPIError(error);
      setLocalError(errorMessage);
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    dispatch({ type: 'SET_INPUT_VALUE', payload: e.target.value });
  };

  return (
    <div className="user-input">
      {(localError || state.error) && (
        <div className="error-message">
          <span className="error-icon">⚠️</span>
          {localError || state.error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="input-form">
        <div className="input-container">
          <textarea
            value={state.inputValue}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here... (Press Enter to send, Shift+Enter for new line)"
            className="message-input"
            disabled={state.isLoading}
            rows={1}
            maxLength={500}
          />
          <button
            type="submit"
            disabled={!state.inputValue.trim() || state.isLoading}
            className="send-button"
            aria-label="Send message"
          >
            {state.isLoading ? (
              <Loader2 size={20} className="spinner" />
            ) : (
              <Send size={20} />
            )}
          </button>
        </div>
        
        <div className="input-footer">
          <span className="character-count">
            {state.inputValue.length}/500
          </span>
          <span className="hint">
            Press Enter to send • Shift+Enter for new line
          </span>
        </div>
      </form>
    </div>
  );
};
