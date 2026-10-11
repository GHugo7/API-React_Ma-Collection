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
        <ul>
            {data.results.map((item) => (
                <li key={item.id}>{item.titre}</li>
            ))}
        </ul>
    )
}
