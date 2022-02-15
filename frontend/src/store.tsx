import { proxy } from "valtio";
import { readLoginStatus } from "./auth/loginStatus";
import { getCurrentUser } from "./services/getCurrentUser";
import { getIdToken } from "./services/getIdToken";
import { getProducts } from "./services/getProducts";
import { getProductsFromUser } from "./services/getProductsFromUser";
import { Product } from "./types/product";
import { Role } from "./types/role";

interface ApplicationState {
    deposit: number;
    role: Role | "";
    products: (Product & { selected?: boolean })[];
    loggedIn: boolean;
}

export const store = proxy<ApplicationState>({
    deposit: 0,
    role: "",
    products: [],
    loggedIn: readLoginStatus(),
});

export const fetchUser = () => {
    getCurrentUser()
        .then(({ data }) => {
            store.deposit = data.deposit;
            store.role = data.role;
        })
        .catch(console.error);
};

export const fetchProducts = () => {
    getProducts()
        .then(({ data }) => {
            store.products = data.products;
        })
        .catch(console.error);
};

export const fetchProductsFromUser = () => {
    getProductsFromUser().then(({ data }) => {
        store.products = data.products;
    });
};

export const saveLoginState = (state: boolean) => {
    store.loggedIn = state;
};

setInterval(() => {
    // Refresh the token every 30 mins
    getIdToken();
}, 1000 * 60 * 30);
