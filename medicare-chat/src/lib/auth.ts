import { apiClient } from './api';

export interface LoginRequest {
  username: string;
  password: string;
}

export interface SignupRequest {
  email: string;
  password: string;
  full_name: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
}

export const authService = {
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    // FastAPI expects OAuth2PasswordRequestForm - form data, not JSON
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await apiClient.postFormData<AuthResponse>('/login', formData);
    
    // Store token in localStorage
    if (response.access_token) {
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('token_type', response.token_type);
    }

    return response;
  },

  async signup(data: SignupRequest): Promise<AuthResponse> {
    // First, create the user account
    await apiClient.post<User>('/signup', data);
    
    // Then automatically log them in
    return this.login({
      username: data.email,
      password: data.password,
    });
  },

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token_type');
  },

  getToken(): string | null {
    return localStorage.getItem('access_token');
  },

  isAuthenticated(): boolean {
    return !!this.getToken();
  },
};
