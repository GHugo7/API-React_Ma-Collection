import type { TokenResponse } from "../types/api";
import { apiFetch } from "./httpClient";

export async function login(email: string, password: string): Promise<TokenResponse> {
    return apiFetch()
}

