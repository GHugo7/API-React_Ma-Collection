import { useState } from "react";

export function useLocalStorage<T>(cle: string, valeurInitiale: T): [T, (v: T) => void] {
    const [ valeur, setValeur ] = useState<T>(() => {
        try {
            const brut = localStorage.getItem(cle);
            return brut === null ? valeurInitiale: (JSON.parse(brut) as T);
        } catch {
            return valeurInitiale;
        }
    });

    const definir = (v: T) => {
        setValeur(v)
        if (v === null) {
            localStorage.removeItem(cle);
        } else {
            localStorage.setItem(cle, JSON.stringify(v))
        }
    };

    return [ valeur, definir ]
}