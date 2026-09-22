import { useState } from "react"
import Button from "../components/ui/Button"
import { useAuth } from "../contexts/AuthContext";
import { Link, useNavigate } from "react-router-dom";

export default function Login() {
    const [ email, setEmail ] = useState("");
    const [ password, setPassword ] = useState("");
    const [ erreur, setErreur ] = useState<string | null>(null);
    const [ chargement, setChargement ] = useState(false);

    const { login } = useAuth();
    const navigate = useNavigate();

    return(
        <form onSubmit={async (e) => {
            e.preventDefault();
            setErreur(null);
            setChargement(true);
            try {
                await login(email, password);
                navigate("/collection")
            } catch(err: unknown) {
                setErreur(err instanceof Error ? err.message : "Erreur inconnue");
            } finally {
                setChargement(false);
            }
        }}
        className="max-w-2xl mx-auto border rounded mt-10 p-8 flex flex-col items-center gap-3">

        <h1 className="text-xl font-bold mb-5">Connexion</h1>
            <label className="grid gap-1 w-72">Adresse mail :
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="border rounded px-2 py-1" required />
            </label>
            <label className="grid gap-1 w-72">Mot de passe :
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="border rounded px-2 py-1" required />
            </label>

            {erreur && 
            <p role="alert" className="text-red-600 text-sm">{erreur}</p>}

            <Button type="submit" variante="primaire" disabled={chargement}>
                {chargement ? "Connexion..." : "Se connecter"}
            </Button>

            <p className="text-sm">
                Pas de compte ? <Link to="/register" className="underline">S'inscrire</Link>
            </p>
        </form>
    )
}