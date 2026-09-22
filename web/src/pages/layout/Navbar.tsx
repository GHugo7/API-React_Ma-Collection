import { Outlet } from "react-router-dom";
import { Link } from "react-router-dom";

export default function Navbar() {
    return(
        <>
        <header className="border-b ">
            <nav className="flex gap-4 items-center px-4 py-3">
                <Link to="/" className="font-bold">Ma Collection</Link>
                <Link to="/login" className="ml-auto">Se connecter</Link>
                <Link to="/register" className="">S'inscrire</Link>
            </nav>
        </header>
        <main className="p-4">
            <Outlet />
        </main>
        </>
    )
}