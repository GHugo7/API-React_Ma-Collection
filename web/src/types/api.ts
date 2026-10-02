// ---------- Auth ----------
export interface User {
  id: number;
  email: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface ApiErrorBody {
  error: {
    code: number;
    message: string;
  };
}