import { useEffect, useState } from "react"
import type { Statut, Entry, Tri } from "../types/api"
import { lister } from "../services/collectionService"
import Button from "../components/ui/Button"

const LABELS: Record<Statut, string> = {
    en_cours: "En cours",
    a_decouvrir: "À découvrir",
    termine: "Terminé"
}

export default function Collection() {
    const [ data, setData ] = useState<Entry[] | null>(null)
    const [ load, setLoad ] = useState(true)
    const [ error, setError ] = useState<string | null>(null)

    const [ statut, setStatut ] = useState<Statut | undefined>(undefined);
    const [ tri, setTri ] = useState<Tri | undefined>(undefined);


    useEffect(() => {
        setLoad(true)
        setError(null)
        lister(statut, tri).then(setData)
        .catch(e => setError(e.message))
        .finally(() => setLoad(false));
    }, [statut, tri])

    if (error) return <p>{error}</p>;

    return(
    <>
    <div>
        <Button variante={statut === "en_cours" ? "primaire" : "secondaire"} onClick={() => setStatut(statut === "en_cours" ? undefined : "en_cours")}>{LABELS.en_cours}</Button>
        <Button variante={statut === "a_decouvrir" ? "primaire" : "secondaire"} onClick={() => setStatut(statut === "a_decouvrir" ? undefined : "a_decouvrir")}>{LABELS.a_decouvrir}</Button>
        <Button variante={statut === "termine" ? "primaire" : "secondaire"} onClick={() => setStatut(statut === "termine" ? undefined : "termine")}>{LABELS.termine}</Button>
        
        <select
            className="ml-5"
            value={tri ?? ""}
            onChange={(e) => {
                const v = e.target.value;
                setTri(v === "" ? undefined : (v as Tri));
            }}
            >
            <option value="">Trier par…</option>
            <option value="date">Date d'ajout</option>
            <option value="note">Note</option>
        </select>

    </div>
        {load ? (
            <p>Chargement...</p>
        ) : !data || data.length === 0 ? (
            <p>Ta collection est vide</p>
        ) : (

        <div className="grid grid-cols-2 md:grid-cols-4 gap-5">
            {data.map((entry) => (
                <article key={entry.id} className="border rounded overflow-hidden">
                    <img src={entry.item.image_url} alt={entry.item.titre} className="w-full" />
                    <div className="p-2">
                        <h2 className="font-bold truncate">{entry.item.titre}</h2>
                        <p className="text-sm text-gray-600">{entry.item.categorie} - {entry.item.annee}</p>
                        <p className="text-sm">{LABELS[entry.statut]}</p>
                        <p className="text-sm">{entry.note ? `${entry.note}/5` : "Non noté"}</p>    
                    </div>
                </article>
            ))}
        </div>
        )}
    </>
    )
}