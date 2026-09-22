import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import type { User } from "../types/api"
import { useLocalStorage } from "../hooks/useLocalStorage";
import * as authService from "../services/authService.mock";

interface AuthContextValue {
    token: string | null,
    user: User | null,
    login: (email: string, password: string) => Promise<void>
    logout: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null);

export const AuthProvider = ({ children }: { children: ReactNode}) => {
    const [ token, setToken ] = useLocalStorage<string | null>("authToken", null);
    const [ user, setUser ] = useState<User | null>(null);

    useEffect(() => {
        if (!token) {
            setUser(null);
            return
        }
        authService.me().then(setUser).catch(() => setUser(null));
    }, [token]);

    async function login(email: string, password: string) { 
        const res = await authService.login(email, password)
        setToken(res.access_token); 
    }

    function logout() { setToken(null); }


    return(
        <AuthContext.Provider value={{ token, user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export function useAuth(): AuthContextValue {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error("useAuth doit être utilisé dans un AuthProvider")
    return ctx;
}