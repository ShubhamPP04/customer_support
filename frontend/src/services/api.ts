import axios from 'axios';
import { Message, Conversation } from '../context/ChatContext';

const API_BASE_URL = 'http://localhost:5001';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ChatResponse {
  response: string;
  conversation_id: string;
  timestamp: string;
}

export interface ConversationHistoryResponse {
  conversation_id: string;
  messages: Array<{
    type: 'user' | 'assistant';
    content: string;
    timestamp: string;
  }>;
}

export const chatAPI = {
  // Send a message to the chatbot
  sendMessage: async (message: string, conversationId?: string): Promise<ChatResponse> => {
    const response = await apiClient.post('/api/chat', {
      message,
      conversation_id: conversationId,
    });
    return response.data;
  },

  // Get conversation history
  getConversationHistory: async (conversationId: string): Promise<ConversationHistoryResponse> => {
    const response = await apiClient.get(`/api/conversations/${conversationId}/history`);
    return response.data;
  },

  // Get all conversations
  getAllConversations: async (): Promise<{ conversations: Array<{
    conversation_id: string;
    created_at: string;
    updated_at: string;
    message_count: number;
  }> }> => {
    const response = await apiClient.get('/api/conversations');
    return response.data;
  },

  // Health check
  healthCheck: async (): Promise<{ status: string; timestamp: string }> => {
    const response = await apiClient.get('/health');
    return response.data;
  },
};

// Utility function to convert API message format to internal format
export const convertAPIMessageToMessage = (
  apiMessage: { type: 'user' | 'assistant'; content: string; timestamp: string },
  index: number
): Message => ({
  id: `msg-${Date.now()}-${index}`,
  type: apiMessage.type,
  content: apiMessage.content,
  timestamp: apiMessage.timestamp,
});

// Error handler
export const handleAPIError = (error: any): string => {
  if (error.response?.data?.error) {
    return error.response.data.error;
  }
  if (error.message) {
    return error.message;
  }
  return 'An unexpected error occurred';
};
