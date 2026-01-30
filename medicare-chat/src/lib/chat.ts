import { apiClient } from './api';
import { Chat, ChatHistoryResponse, Message } from '@/types/chat';

export const chatService = {
  async getChatHistory(): Promise<ChatHistoryResponse[]> {
    return apiClient.get<ChatHistoryResponse[]>('/chats/');
  },

  async getChat(chatId: string): Promise<Chat> {
    return apiClient.get<Chat>(`/chats/${chatId}`);
  },

  async createChat(title: string, message: string): Promise<Chat> {
    return apiClient.post<Chat>('/chats/', { title, message });
  },

  async addMessageToChat(chatId: string, message: string): Promise<Message> {
    return apiClient.post<Message>(`/chats/${chatId}/messages`, { content: message });
  },

  async deleteChat(chatId: string): Promise<void> {
    return apiClient.delete<void>(`/chats/${chatId}`);
  },
};
