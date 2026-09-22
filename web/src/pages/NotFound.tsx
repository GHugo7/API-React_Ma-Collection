import { Link } from "react-router-dom"
import gargaros from '../assets/img/Gargaros.png'

export default function NotFound() {
    return(
        <>
        <div className="min-h-screen flex flex-col items-center justify-start gap-8 p-8">
        <h1 className="text-5xl font-bold">404 Not Found</h1>

        <div className="grid w-full grid-cols-1 md:grid-cols-3 items-center gap-6 justify-items-center">
            <img src={gargaros} alt="Gargaros Yokai-Watch" className="max-w-xs md:justify-self-start" />
            <div className="flex flex-col gap-2 text-center">
                <p className="font-bold">TU AS ENFREINT LES RÈGLES !</p>
                <p><Link to="/" className="underline">Casse toi</Link> de chez moi !</p>
            </div>
        </div>
        </div>
        </>
    )
}