/**
 * مدل‌های کاربر
 */

export interface User {
  username: string;
  email: string;
  full_name?: string;
  is_active?: boolean;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  full_name?: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface RegisterResponse {
  username: string;
  email: string;
  full_name?: string;
  message: string;
}
