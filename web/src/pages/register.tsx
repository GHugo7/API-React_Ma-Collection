import { useState } from "react";
import Button from "../components/button";

export default function Register() {
    const [ prenom, setPrenom ] = useState("");
    const [ nom, setNom ] = useState("");
    const [ email, setEmail] = useState("");
    const [ password, setPassword] = useState("");
    const [ confirm, setConfirm ] = useState("");

    const differents = confirm !== "" && password !== confirm;

    return(
        <div className="">
            <form onSubmit={(e) => {e.preventDefault(); alert(`Nom soumis : ${nom}`)}} className="block w-full border rounded px-2 py-1">
                <div className="flex justify-center gap-3 mr-10">
                    <label className="">Prenom:
                        <input type="text" value={prenom} onChange={(e) => setPrenom(e.target.value)} className="border ml-2" required />
                    </label>
                    <label className="">Nom:
                        <input type="text" value={nom} onChange={(e) => setNom(e.target.value)} className="border ml-2" required />
                    </label>
                </div>
                <label className="block mb-3 mt-3">Adresse e-mail:
                    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="border ml-2" required />
                </label>
                <label className="block mb-3">Mot de passe:
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="border ml-2" required />
                </label>
                <label className="block mb-3">Confirmer le mot de passe:
                    <input type="password" value={confirm} onChange={(e) => setConfirm(e.target.value)} aria-invalid={differents} className="border ml-2" required />
                </label>
                {differents && <p role="alert">Les mots de passes sont differents</p>}
                <Button type="submit" variante="primaire">S'inscrire</Button>
            </form>
        </div>
    )
}