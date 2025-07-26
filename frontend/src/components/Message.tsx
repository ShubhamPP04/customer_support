import React from 'react';
import { Message as MessageType } from '../context/ChatContext';
import { User, Bot } from 'lucide-react';
import './Message.css';

interface MessageProps {
  message: MessageType;
}

export const Message: React.FC<MessageProps> = ({ message }) => {
  const isUser = message.type === 'user';

  // Function to render text with markdown-style bold formatting
  const renderContent = (content: string) => {
    // Split by ** and make every odd index bold
    const parts = content.split('**');
    return parts.map((part, index) => {
      if (index % 2 === 1) {
        return <strong key={index}>{part}</strong>;
      }
      return part;
    });
  };

  return (
    <div className={`message ${isUser ? 'message-user' : 'message-assistant'}`}>
      <div className={`message-avatar ${isUser ? 'user-avatar' : 'bot-avatar'}`}>
        {isUser ? (
          <User size={22} className="avatar-icon" />
        ) : (
          <Bot size={22} className="avatar-icon" />
        )}
      </div>
      <div className="message-content">
        <div className="message-text">
          {renderContent(message.content)}
        </div>
      </div>
    </div>
  );
};
