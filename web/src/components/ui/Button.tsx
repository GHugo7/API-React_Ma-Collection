import type { ButtonHTMLAttributes } from "react"
import '../../App.css';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    variante?: "primaire" | "secondaire" | "danger";
}

export default function Button({variante = "primaire", type="button", ...rest}: ButtonProps) {
    return <button type={type} className={`btn btn-${variante}`} {...rest} />
}