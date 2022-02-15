export function saveLoginStatus(status: boolean) {
    localStorage.setItem("loggedIn", JSON.stringify({ status }));
}

export function readLoginStatus() {
    const localStorageLoginStatus = localStorage.getItem("loggedIn");
    const status = localStorageLoginStatus
        ? JSON.parse(localStorageLoginStatus).status
        : false;

    return Boolean(status);
}
