import { useEffect } from "react";
import { useSnapshot } from "valtio";
import { fetchProducts, store } from "../store";

function useProducts() {
    const { products } = useSnapshot(store);

    useEffect(() => {
        fetchProducts();
    }, []);

    return { products };
}

export default useProducts;
