import { useEffect } from "react";
import { useSnapshot } from "valtio";
import { fetchUser, store } from "../store";

function useUser() {
    const { role, deposit } = useSnapshot(store);

    useEffect(() => {
        fetchUser();
    }, []);

    return { role, deposit };
}

export default useUser;
