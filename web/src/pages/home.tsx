import { Link } from "react-router-dom";

export default function Home() {
    return(
        <div className="">
            <Link to="/register">S'inscrire</Link>
            <Link to="/login">Se connecter</Link>
        </div>
    )
}