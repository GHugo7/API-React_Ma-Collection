import { useState } from "react";
import Button from "../components/ui/Button";
import { Link, useNavigate } from "react-router-dom";
import * as authService from "../services/authService.mock"

export default function Register() {
    const [ email, setEmail] = useState("");
    const [ password, setPassword] = useState("");
    const [ confirm, setConfirm ] = useState("");
    const [ chargement, setChargement ] = useState(false);
    const [ erreur, setErreur ] = useState<string | null>(null);

    const differents = confirm !== "" && password !== confirm;

    const navigate = useNavigate();

    return(
        <div className="min-h-[75vh] flex items-center justify-center">
            <form onSubmit={async (e) => {
                e.preventDefault();
                setErreur(null);
                setChargement(true);
                try {
                    await authService.register(email, password);
                    navigate("/login");
                } catch (err: unknown) {
                    setErreur(err instanceof Error ? err.message : "Erreur inconnue");
                } finally {
                    setChargement(false);
                }
        }} className="max-w-md mx-auto border rounded-lg shadow-sm bg-white mt-10 p-8 flex flex-col items-center gap-3">
                <h1 className="text-xl font-bold mb-5">Créer un compte</h1> 
                <label className="grid gap-1 w-72">Adresse e-mail :
                    <input type="email" value={email} placeholder="vous@example.fr" onChange={(e) => setEmail(e.target.value)} className="border rounded px-2 py-1" required />
                </label>
                <label className="grid gap-1 w-72">Mot de passe :
                    <input type="password" value={password} minLength={8} onChange={(e) => setPassword(e.target.value)} className="border rounded px-2 py-1" required />
                    <p className="text-sm text-gray-600">8 caractères minimum</p>
                </label>
                <label className="grid gap-1 w-72">Confirmer le mot de passe :
                    <input type="password" value={confirm} onChange={(e) => setConfirm(e.target.value)} aria-invalid={differents} className="border rounded px-2 py-1" required />
                </label>

                {differents && <p role="alert" className="text-red-600 text-sm">Les mots de passe sont differents</p>}
                {erreur && <p role="alert" className="text-red-600 text-sm">{erreur}</p>}


                <Button type="submit" variante="primaire" className="w-full" disabled={chargement || differents}>{ chargement ? "Inscription..." : `S'inscrire`}</Button>

                <p className="text-sm">
                    Déjà un compte ? <Link to="/login" className="underline">Se connecter</Link>
                </p>
            </form>
        </div>
    )
}