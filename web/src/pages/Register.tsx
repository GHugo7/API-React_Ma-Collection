import { useState, type FormEvent } from "react";
import Button from "../components/ui/Button";

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
        <form onSubmit={submit} className="max-w-4xl mx-auto border rounded mt-10 p-8 flex flex-col items-center gap-3">
            <label className="block mb-1 mt-3 ml-18 mr-12">Nom:
                <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} className="border ml-2" required />
            </label>
            <label className="block mb-3 mt-3 mr-12">Adresse e-mail:
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="border ml-2" required />
            </label>
            <label className="block mb-3 ml-2.5 mr-11.5">Mot de passe:
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="border ml-2" required />
            </label>
            <label className="block mb-3 mr-34">Confirmer le mot de passe:
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