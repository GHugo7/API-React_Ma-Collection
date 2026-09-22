import { useState, type FormEvent } from "react";
import Button from "../components/ui/Button";

export default function Register() {
    const [ email, setEmail] = useState("");
    const [ password, setPassword] = useState("");
    const [ confirm, setConfirm ] = useState("");

    const differents = confirm !== "" && password !== confirm;

    const submit = (e: FormEvent<HTMLFormElement>) => {
        if (differents) return
        e.preventDefault();
        alert(`Email soumis : ${email}`)
    }

    return(
        <form onSubmit={submit} className="max-w-4xl mx-auto border rounded mt-10 p-8 flex flex-col items-center gap-3">
            <h1 className="text-xl font-bold mb-5">Créer un compte</h1> 
            <label className="grid gap-1 w-72">Adresse e-mail:
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="border rounded px-2 py-1" required />
            </label>
            <label className="grid gap-1 w-72">Mot de passe:
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="border rounded px-2 py-1" required />
            </label>
            <label className="grid gap-1 w-72">Confirmer le mot de passe:
                <input type="password" value={confirm} onChange={(e) => setConfirm(e.target.value)} aria-invalid={differents} className="border rounded px-2 py-1" required />
            </label>

            {differents && <p role="alert">Les mots de passes sont differents</p>}

            <Button type="submit" variante="primaire">S'inscrire</Button>
        </form>
    )
}