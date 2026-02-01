import { apiClient } from './api';

export interface UserProfile {
  user_id: string;
  email: string;
  full_name: string;
  created_at: string;
  age?: number;
  gender?: string;
  health_summary?: string;
  medical_conditions?: string[];
  last_summary_update?: string;
}

export interface UserUpdate {
  full_name?: string;
  age?: number;
  gender?: string;
}

export interface HealthSummaryResponse {
  summary: string;
  medical_conditions: string[];
  last_updated: string;
}

export interface DocumentResponse {
  document_id: string;
  user_id: string;
  filename: string;
  file_type: string;
  file_size: number;
  description?: string;
  extracted_text?: string;
  processed: boolean;
  uploaded_at: string;
}
export const userService = {
  async getCurrentUser(): Promise<UserProfile | null> {
    try {
      return await apiClient.get<UserProfile>('/users/me');
    } catch (error) {
      return null;
    }
  },

  async updateCurrentUser(data: UserUpdate): Promise<UserProfile> {
    return apiClient.put<UserProfile>('/users/me', data);
  },

  async generateHealthSummary(): Promise<HealthSummaryResponse> {
    return apiClient.post<HealthSummaryResponse>('/users/me/health-summary', {});
  },

  async getHealthSummary(): Promise<HealthSummaryResponse> {
    return apiClient.get<HealthSummaryResponse>('/users/me/health-summary');
  },

  async getDocuments(): Promise<DocumentResponse[]> {
    try {
      return await apiClient.get<DocumentResponse[]>('/documents/');
    } catch (error) {
      console.error('Failed to fetch documents:', error);
      return [];
    }
  },

  async uploadDocument(formData: FormData): Promise<DocumentResponse> {
    return apiClient.postFormData<DocumentResponse>('/documents/upload', formData);
  },

  async deleteDocument(documentId: string): Promise<void> {
    return apiClient.delete<void>(`/documents/${documentId}`);
  },
};
