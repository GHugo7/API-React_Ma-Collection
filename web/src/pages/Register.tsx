import { useState, type FormEvent } from "react";
import Button from "../components/ui/button";

export default function Register() {
    const [ username, setUsername ] = useState("");
    const [ email, setEmail] = useState("");
    const [ password, setPassword] = useState("");
    const [ confirm, setConfirm ] = useState("");

    const differents = confirm !== "" && password !== confirm;

    const submit = (e: FormEvent<HTMLFormElement>) => {
        if (differents) return
        e.preventDefault();
        alert(`Nom soumis : ${username}`)
    }

    return(
        <>
        <form onSubmit={submit} className="block w-full border rounded px-2 py-1">
            <label className="block mb-3 mt-3 ml-18 md:mr-25">Nom:
                <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} className="border ml-2" required />
            </label>
            <label className="block mb-3 mt-3 md:mr-25.5">Adresse e-mail:
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="border ml-2" required />
            </label>
            <label className="block mb-3 ml-2.5 mr-25.5">Mot de passe:
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="border ml-2" required />
            </label>
            <label className="block mb-3 md:mr-48">Confirmer le mot de passe:
                <input type="password" value={confirm} onChange={(e) => setConfirm(e.target.value)} aria-invalid={differents} className="border ml-2" required />
            </label>
            {differents && <p role="alert">Les mots de passes sont differents</p>}
            <div className="ml-2">
                <Button type="submit" variante="primaire">S'inscrire</Button>
            </div>
        </form>
        </>
    )
}