import { apiFetch } from "./httpClient";
import type { Entry, EntryCreate, EntryUpdate, Stats, Statut, Tri } from "../types/api"

export async function lister(statut?: Statut, tri?: Tri): Promise<Entry[]> {
    const params = new URLSearchParams();
    if (statut) params.set("statut", `${statut}`);
    if (tri) params.set("tri", `${tri}`)

    return apiFetch<Entry[]>(`/me/collection?${params}`)
}

export async function add(data: EntryCreate): Promise<Entry> {
    return apiFetch<Entry>("/me/collection", { method: "POST", body: JSON.stringify( data ) })
}

export async function modify(id: number, data: EntryUpdate): Promise<Entry> {
    return apiFetch<Entry>(`/me/collection/${id}`, { method: "PATCH", body: JSON.stringify( data ) })
}

export async function del(id: number): Promise<void> {
    return apiFetch<void>(`/me/collection/${id}`, { method: "DELETE" });
}

export async function stats(): Promise<Stats> {
    return apiFetch<Stats>("/me/stats")
}