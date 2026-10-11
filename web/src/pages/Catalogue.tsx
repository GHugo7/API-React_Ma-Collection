import { useEffect, useState } from "react";
import { lister } from "../services/itemsService";
import type { ItemPage } from "../types/api";

export default function Catalogue() {
    const [ data, setData ] = useState<ItemPage | null>(null);
    const [ load, setLoad ] = useState(true);
    const [ error, setError ] = useState<string | null>(null);

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
        <div className="grid grid-cols-2 md:grid-cols-4 gap-5">
            {data.results.map((item) => (
                <article key={item.id} className="border rounded overflow-hidden">
                    <img src={item.image_url} alt={item.titre} className="w-full" />
                    <div className="p-2">
                        <h2 className="font-bold truncate">{item.titre}</h2>
                        <p className="text-sm text-gray-600">{item.categorie} - {item.annee}</p>
                    </div>
                </article>
            ))}
        </div>
    )
}
