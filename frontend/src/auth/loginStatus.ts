import { saveLoginState } from "../store";

export function saveLoginStatus(status: boolean) {
    localStorage.setItem("loggedIn", JSON.stringify({ status }));
    saveLoginState(status);
}

export function readLoginStatus() {
    const localStorageLoginStatus = localStorage.getItem("loggedIn");
    const status = localStorageLoginStatus
        ? JSON.parse(localStorageLoginStatus).status
        : false;

    return Boolean(status);
}
