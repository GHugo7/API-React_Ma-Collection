import { useState, type FormEvent } from "react"
import Button from "../components/ui/button"

export default function Login() {
    const [ email, setEmail ] = useState("");
    const [ password, setPassword ] = useState("");
 
    const submit = (e: FormEvent<HTMLFormElement>) => { 
        e.preventDefault();
        alert(`Le nom d'utilisateur est ${email}\nMot de passe ${password}`)
     }

    return(
        <>
        <form onSubmit={submit} className="block w-full border rounded px-2 py-1">
            <label className="block mb-3 mt-3 md:mr-25.5">Nom ou email:
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="border ml-2" required />
            </label>
            <label className="block mb-3 ml-2.5 mr-25.5">Mot de passe:
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="border ml-2" required />
            </label>
            <div className="ml-2">
                <Button type="submit" variante="primaire">Se connecter</Button>
            </div>
        </form>
        </>
    )
}