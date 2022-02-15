import { useEffect } from "react";
import { fetchFunds, store } from "../store";

function Funds() {
    useEffect(() => {
        fetchFunds();
    }, []);

    return <div>{store.funds} credits</div>;
}

export default Funds;
