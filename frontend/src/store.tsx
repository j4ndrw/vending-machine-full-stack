import { proxy } from "valtio";
import { getCurrentUser } from "./services/getCurrentUser";
import { getIdToken } from "./services/getIdToken";

interface ApplicationState {
    funds: number;
}

export const store = proxy<ApplicationState>({
    funds: 0,
});

export const fetchFunds = () => {
    getCurrentUser()
        .then(({ data }) => {
            store.funds = data.deposit;
        })
        .catch(console.error);
};

setInterval(() => {
    // Refresh the token every 30 mins
    getIdToken();
}, 1000 * 60 * 30);
