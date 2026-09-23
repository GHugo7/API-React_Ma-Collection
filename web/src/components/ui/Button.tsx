import type { ButtonHTMLAttributes } from "react"

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    variante?: "primaire" | "secondaire" | "danger";
}

const variantes = {
  primaire: "bg-indigo-600 text-white hover:bg-indigo-700",
  secondaire: "bg-transparent text-indigo-600 border border-indigo-600 hover:bg-indigo-50",
  danger: "bg-red-600 text-white hover:bg-red-700",
};


export default function Button({
    variante = "primaire", 
    type="button",
    className="",
    ...rest
}: ButtonProps) {
    return(
      <button 
        type={type} 
        className={`px-4 py-2 rounded-lg cursor-pointer transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${variantes[variante]} ${className}`} 
        {...rest} 
      />
    );
}