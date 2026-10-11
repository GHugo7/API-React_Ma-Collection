import { useEffect, useState } from "react";
import { lister } from "../services/itemsService";
import type { ItemPage } from "../types/api";

export default function Catalogue() {
    const [ data, setData ] = useState<ItemPage | null>(null);
    const [ load, setLoad ] = useState(true);
    const [ error, setError ] = useState<string | null>(null);

    useEffect(() => {
        setLoad(true);
        setError(false);
        lister(1, 12)
            .then(setData)
            .catch((e) => setError(e.message))
            .finally(() => setLoad(false));
    }, []);

    return(
        <div className="">
            <ul>
                
            </ul>   
        </div>
    )
}
