import { useEffect } from "react";
import { useSnapshot } from "valtio";
import { fetchProductsFromUser, store } from "../store";

function useSellerProducts() {
    const { products } = useSnapshot(store);

    useEffect(() => {
        fetchProductsFromUser();
    }, []);

    return { products };
}

export default useSellerProducts;
