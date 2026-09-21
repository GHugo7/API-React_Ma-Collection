import { type FormEvent } from "react"
import Button from "../components/button"

export default function Login() {

    const submit = (e: FormEvent<HTMLFormElement>) => {  }

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
                <Button type="submit" variante="primaire">S'inscrire</Button>
            </div>
        </form>
        </>
    )
}