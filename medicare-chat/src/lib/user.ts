import { apiClient } from './api';

export interface UserProfile {
  user_id: string;
  email: string;
  full_name: string;
  created_at: string;
}

export interface UserUpdate {
  full_name?: string;
}

export interface Patient {
  patient_id: string;
  name: string;
  age: number;
  gender: string;
  blood_group?: string;
  height?: number;
  weight?: number;
  phone: string;
  email?: string;
  address?: string;
  emergency_contact?: string;
  health_info: {
    allergies?: string[];
    chronic_conditions?: string[];
    current_medications?: string[];
    previous_surgeries?: string[];
    family_history?: string[];
  };
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface PatientCreate {
  name: string;
  age: number;
  gender: string;
  phone: string;
  email?: string;
}

export interface PatientUpdate {
  name?: string;
  age?: number;
  gender?: string;
  phone?: string;
  email?: string;
}

export interface Document {
  document_id: string;
  patient_id: string;
  document_type: string;
  title: string;
  file_name: string;
  file_size: number;
  mime_type: string;
  upload_date: string;
  uploaded_by: string;
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

  async getPatients(): Promise<Patient[]> {
    try {
      return await apiClient.get<Patient[]>('/patients/');
    } catch (error) {
      console.error('Failed to fetch patients:', error);
      return [];
    }
  },

  async createPatient(patientData: PatientCreate): Promise<Patient> {
    return apiClient.post<Patient>('/patients/', patientData);
  },

  async updatePatient(patientId: string, patientData: PatientUpdate): Promise<Patient> {
    return apiClient.put<Patient>(`/patients/${patientId}`, patientData);
  },

  async deletePatient(patientId: string): Promise<void> {
    return apiClient.delete<void>(`/patients/${patientId}`);
  },

  async getDocuments(patientId?: string): Promise<Document[]> {
    try {
      if (patientId) {
        return await apiClient.get<Document[]>(`/documents/patient/${patientId}`);
      }
      return [];
    } catch (error) {
      console.error('Failed to fetch documents:', error);
      return [];
    }
  },

  async uploadDocument(formData: FormData): Promise<Document> {
    return apiClient.postFormData<Document>('/documents/upload', formData);
  },

  async deleteDocument(documentId: string): Promise<void> {
    return apiClient.delete<void>(`/documents/${documentId}`);
  },
};
