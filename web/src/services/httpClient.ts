import type { ApiErrorBody } from "../types/api";

const env = import.meta.env.VITE_API_URL;

function readToken(): string | null {
    const brut = localStorage.getItem("authToken");
    if (!brut) return null

    try {
        const parse: unknown = JSON.parse(brut)
        return typeof parse === "string" ? parse : null;
    } catch {
        return null
    }
}

function isAPIError(data: unknown): data is ApiErrorBody {
    return typeof data === "object" && data !== null && "error" in data;
}

export async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
    const token = readToken();
    let data: unknown = null;

    const response = await fetch(env + path, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
            ...options?.headers,
        },
    });

    try {
        data = await response.json()
    } catch {}
    
    if (!response.ok) {
        if (isAPIError(data)) {
            throw new Error(data.error.message)
        } else {
            throw new Error("Une erreur inhabituelle est survenue")
        }
    }
    
    if (response.status === 204)
        return undefined as T
    else {
        return data as T
    }
}