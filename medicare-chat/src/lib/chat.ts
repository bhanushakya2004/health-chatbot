import { apiClient } from './api';
import { Chat, ChatHistoryResponse, Message } from '@/types/chat';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

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

  async streamMessage(
    chatId: string,
    message: string,
    onChunk: (chunk: string) => void,
    onComplete?: () => void,
    onError?: (error: Error) => void
  ): Promise<void> {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('No authentication token found');
    }

    try {
      const response = await fetch(`${API_URL}/chats/${chatId}/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ content: message }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('Response body is not readable');
      }

      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        
        if (done) {
          onComplete?.();
          break;
        }

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            
            if (data === '[DONE]') {
              onComplete?.();
              return;
            }

            try {
              const parsed = JSON.parse(data);
              if (parsed.chunk) {
                onChunk(parsed.chunk);
              } else if (parsed.error) {
                onError?.(new Error(parsed.error));
              }
            } catch (e) {
              console.warn('Failed to parse SSE data:', data);
            }
          }
        }
      }
    } catch (error) {
      onError?.(error as Error);
      throw error;
    }
  },
};
