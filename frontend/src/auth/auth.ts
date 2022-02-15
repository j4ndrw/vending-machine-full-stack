export function storeCredentials(token: string, username: string = "") {
    // I'm aware you're not supposed to store JWTs in the browser.
    // Ideally, you should split the JWT into 2, such that you
    // store the payload in a cookie, and the signature in another cookie.
    // and then reconstruct the JWT in the backend.

    // Though, since this is a small app, I'll store the whole thing
    // in document.cookie for now, along with the current
    // user

    document.cookie = JSON.stringify({
        token,
        username,
    });
}

export function readCredentials(): { token: string; username: string } {
    try {
        return JSON.parse(document.cookie);
    } catch (e) {
        console.error(e);
        return { token: "", username: "" };
    }
}
