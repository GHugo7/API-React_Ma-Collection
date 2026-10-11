import { Outlet, Link } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";
import Button from "../../components/ui/Button";

export default function Navbar() {
    const { user, logout } = useAuth();

    return(
        <>
        <header className="border-b ">
            <nav className="flex gap-4 items-center px-4 py-3">
                <Link to="/" className="font-bold">Ma Collection</Link>
                {user ? 
                    <>
                        <Link to="/collection" className="ml-auto">Mon profil</Link>
                        <Button onClick={logout}>Se deconnecter</Button>
                    </>
                    : 
                    <>
                        <Link to="/login" className="ml-auto">Se connecter</Link>
                        <Link to="/register" >S'inscrire</Link>
                    </>
                }
            </nav>
        </header>
        <main className="p-4">
            <Outlet />
        </main>
        </>
    )
}