import type { Item, ItemPage } from "../types/api";
import { apiFetch } from "./httpClient";

export async function lister(page: number, limit: number, q?: string, categorie?: string): Promise<ItemPage> {
    const params = new URLSearchParams();
    params.set("page", `${page}`);
    params.set("limit", `${limit}`);
    if (q) params.set("q", `${q}`);
    if (categorie) params.set("categorie", `${categorie}`)

    return apiFetch<ItemPage>(`/items?${params}`)
}

export async function byId(id: number): Promise<Item> {
    return apiFetch<Item>(`/items/${id}`)
}