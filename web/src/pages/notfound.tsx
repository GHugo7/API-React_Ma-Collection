import { Link } from "react-router-dom"
import gargaros from '../assets/img/Gargaros.png'

export default function NotFound() {
    return(
        <>
        <h1>404 Not Found</h1>
        <div className="gargaros-ref">
            <img src={gargaros} alt="Gargaros Yokai-Watch" className="gargaros" />
            <p className="gargaros-p"><strong>TU AS ENFREINT LES RÈGLES !</strong></p>
            <p><Link to='/'>Casse toi</Link> de chez moi !</p>  
        </div>
        </>
    )
}