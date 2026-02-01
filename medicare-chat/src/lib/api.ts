// API Configuration and Base Setup
import { logApiRequest, logApiError } from './logger';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

interface ApiError {
  message: string;
  detail?: string;
}

class ApiClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    const token = localStorage.getItem('access_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
  }

  private async handleResponse<T>(response: Response, method: string, endpoint: string, startTime: number): Promise<T> {
    const duration = (Date.now() - startTime) / 1000;
    
    if (!response.ok) {
      // Handle 401 Unauthorized - token expired or invalid
      if (response.status === 401) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('token_type');
        window.dispatchEvent(new CustomEvent('auth:unauthorized'));
        logApiError(method, endpoint, new Error('Unauthorized - Please login again'));
        throw new Error('Your session has expired. Please login again.');
      }

      // Handle 403 Forbidden
      if (response.status === 403) {
        logApiError(method, endpoint, new Error('Forbidden'));
        throw new Error('You do not have permission to perform this action.');
      }

      const error: ApiError = await response.json().catch(() => ({
        message: 'An error occurred',
      }));
      
      const errorMsg = error.detail || error.message || 'Request failed';
      logApiError(method, endpoint, new Error(errorMsg));
      throw new Error(errorMsg);
    }

    logApiRequest(method, endpoint, response.status, duration);
    return response.json();
  }

  async get<T>(endpoint: string): Promise<T> {
    const startTime = Date.now();
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'GET',
      headers: this.getHeaders(),
    });

    return this.handleResponse<T>(response, 'GET', endpoint, startTime);
  }

  async post<T>(endpoint: string, data: unknown): Promise<T> {
    const startTime = Date.now();
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    });

    return this.handleResponse<T>(response, 'POST', endpoint, startTime);
  }

  async postFormData<T>(endpoint: string, formData: FormData): Promise<T> {
    const startTime = Date.now();
    const token = localStorage.getItem('access_token');
    const headers: HeadersInit = {};
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      headers,
      body: formData,
    });

    return this.handleResponse<T>(response, 'POST', endpoint, startTime);
  }

  async put<T>(endpoint: string, data: unknown): Promise<T> {
    const startTime = Date.now();
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    });

    return this.handleResponse<T>(response, 'PUT', endpoint, startTime);
  }

  async delete<T>(endpoint: string): Promise<T> {
    const startTime = Date.now();
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    });

    return this.handleResponse<T>(response, 'DELETE', endpoint, startTime);
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
export { API_BASE_URL };
