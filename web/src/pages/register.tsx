import { useState } from "react";
import { Link } from "react-router-dom";
import Button from "../components/button";

export default function Register() {
    const [ email, setEmail] = useState("");
    const [ password, setPassword] = useState("");
    const [ confirm, setConfirm ] = useState("");

    const differents = confirm !== "" && password !== confirm;

    return(
        <div className="">
            <Link to="/">home</Link>
            <form >
                <label>Adresse e-mail:
                    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                </label>
                <label>Mot de passe
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                </label>
                <label>Confirme
                    <input type="password" value={confirm} onChange={(e) => setConfirm(e.target.value)} aria-invalid={differents} required />
                </label>
                {differents && <p role="alert">Les mots de passes sont differents</p>}
            </form>
            <Button type="submit" variante="primaire">S'inscrire</Button>
        </div>
    )
}