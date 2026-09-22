import type { User, TokenResponse } from "../types/api";

const utilisateurs = [{ id: 1, email: "test@test.fr", password: "azerty123" }];

export async function login(email: string, password: string): Promise<TokenResponse> {
  await new Promise((r) => setTimeout(r, 300)); // simule la latence réseau
  const u = utilisateurs.find((x) => x.email === email && x.password === password);
  if (!u) throw new Error("Identifiants invalides");
  return { access_token: "faux-token-" + u.id, token_type: "bearer" };
}

export async function me(): Promise<User> {
  return { id: 1, email: "test@test.fr" };
}