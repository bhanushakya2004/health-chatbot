export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  attachments?: Attachment[];
}

export interface Attachment {
  id: string;
  name: string;
  type: 'pdf' | 'image';
  size: string;
}

export interface Chat {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}

export interface MedicalRecord {
  id: string;
  name: string;
  date: Date;
  fileType: 'pdf' | 'jpg' | 'png';
  size: string;
}

export interface UserProfile {
  name: string;
  email: string;
  age: number;
  gender: 'male' | 'female' | 'other';
  avatar?: string;
}
