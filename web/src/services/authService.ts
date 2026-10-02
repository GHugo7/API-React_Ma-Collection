import type { TokenResponse, User } from "../types/api";
import { apiFetch } from "./httpClient";

export async function login(email: string, password: string): Promise<TokenResponse> {
    return apiFetch<TokenResponse>('/auth/login', {
        method: "POST",
        body: JSON.stringify({ email, password })
    });
}

export async function register(email: string, password: string): Promise<User> {
    return apiFetch<User>('/auth/register', {
        method: "POST",
        body: JSON.stringify({ email, password })
    });
}

export async function me(): Promise<User> {
    return apiFetch<User>('/auth/me')
}