import { useState } from "react"
import Button from "../components/ui/Button"
import { useAuth } from "../contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import "../index.css"

export default function Login() {
    const [ email, setEmail ] = useState("");
    const [ password, setPassword ] = useState("");
    const [ erreur, setErreur ] = useState<string | null>(null);
    const [ chargement, setChargement ] = useState(false);

    const { login } = useAuth();
    const navigate = useNavigate();

    return(
        <>
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

            <label className="block mb-3 mt-3 mr-13">Nom ou email:
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="border ml-2" required />
            </label>
            <label className="block mb-3 ml-2.5 mr-14">Mot de passe:
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="border ml-2" required />
            </label>
            <div className="ml-10">
                <Button type="submit" variante="primaire" disabled={chargement}>{chargement ? "Connexion..." : "Se connecter"}</Button>
            </div>
        </form>
        </>
    )
}