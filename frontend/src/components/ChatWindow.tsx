import React, { useState } from 'react';
import { ConversationHistory } from './ConversationHistory';
import { MessageList } from './MessageList';
import { UserInput } from './UserInput';
import { Menu, X } from 'lucide-react';
import './ChatWindow.css';

export const ChatWindow: React.FC = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="chat-window">
      {/* Mobile sidebar overlay */}
      {isSidebarOpen && (
        <div 
          className="sidebar-overlay"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      {/* Conversation History Sidebar */}
      <div className={`sidebar ${isSidebarOpen ? 'sidebar-open' : ''}`}>
        <ConversationHistory />
      </div>

      {/* Main Chat Area */}
      <div className="main-chat">
        {/* Chat Header */}
        <div className="chat-header">
          <button 
            className="sidebar-toggle"
            onClick={toggleSidebar}
            aria-label="Toggle conversation history"
          >
            {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
          
          <div className="header-content">
            <div className="header-title">
              <span className="app-icon">🤖</span>
              <div>
                <h1>Customer Support Assistant</h1>
                <p>Ask me about orders, products, and inventory</p>
              </div>
            </div>
            
            <div className="status-indicator">
              <div className="status-dot online"></div>
              <span>Online</span>
            </div>
          </div>
        </div>

        {/* Messages Area */}
        <div className="messages-area">
          <MessageList />
        </div>

        {/* Input Area */}
        <div className="input-area">
          <UserInput />
        </div>
      </div>
    </div>
  );
};
