import { useEffect, useState } from "react";
import { lister } from "../services/itemsService";
import type { ItemPage } from "../types/api";
import Button from "../components/ui/Button";
import { add } from "../services/collectionService";
import { useAuth } from "../contexts/AuthContext";

export default function Catalogue() {
    const [ data, setData ] = useState<ItemPage | null>(null);
    const [ load, setLoad ] = useState(true);
    const [ error, setError ] = useState<string | null>(null);
    const [ message, setMessage ] = useState<string | null>(null);
    const { user }  = useAuth();

    async function ajouter(itemId: number) {
        setMessage(null);
        try {
            await add({ item_id: itemId, statut: "a_decouvrir" });
            setMessage("Ajouté à ta collection");
        } catch (e) {
            setMessage(e instanceof Error ? e.message : "Erreur inconnue")
        }
    }

    useEffect(() => {
        setLoad(true);
        setError(null);
        lister(1, 12)
            .then(setData)
            .catch((e) => setError(e.message))
            .finally(() => setLoad(false));
    }, []);

    if (load) return <p>Chargement...</p>;
    if (error) return <p>{error}</p>;
    if (!data || data.total === 0) return <p>Aucun jeu charge</p>;

    return(
        <>
        {message && (
            <p className="mb-4 rounded-lg bg-green-50 border border-green-300 px-4 py-2 text-green-800">{message}</p>
        )}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-5">
            {data.results.map((item) => (
                <article key={item.id} className="border rounded overflow-hidden">
                    <img src={item.image_url} alt={item.titre} className="w-full" />
                    <div className="p-2">
                        <h2 className="font-bold truncate">{item.titre}</h2>
                        <p className="text-sm text-gray-600">{item.categorie} - {item.annee}</p>
                        {user && (
                            <Button onClick={() => ajouter(item.id)}>Ajouter</Button>
                        )}
                    </div>
                </article>
            ))}
        </div>
        </>
    )
}