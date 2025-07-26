import React, { useEffect, useRef } from 'react';
import { useChat } from '../context/ChatContext';
import { Message } from './Message';
import './MessageList.css';

export const MessageList: React.FC = () => {
  const { state } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [state.messages]);

  if (state.messages.length === 0) {
    return (
      <div className="message-list empty">
        <div className="empty-state">
          <div className="empty-icon">💬</div>
          <h3>Welcome to Customer Support</h3>
          <p>
            I'm here to help you with your orders, products, and any questions you might have.
            <br />
            Try asking me about:
          </p>
          <ul>
            <li>"What are the top selling products?"</li>
            <li>"Show me the status of order 12345"</li>
            <li>"How many Classic T-Shirts are in stock?"</li>
          </ul>
        </div>
      </div>
    );
  }

  return (
    <div className="message-list">
      <div className="messages-container">
        {state.messages.map((message) => (
          <Message key={message.id} message={message} />
        ))}
        {state.isLoading && (
          <div className="typing-indicator">
            <div className="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <span className="typing-text">AI is typing...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};
