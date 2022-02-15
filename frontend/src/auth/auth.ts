export function storeCredentials(token: string, username: string = "") {
    // I'm aware you're not supposed to store JWTs in the browser.
    // Ideally, you should split the JWT into 2, such that you
    // store the payload in a cookie, and the signature in another cookie.
    // and then reconstruct the JWT in the backend.

    // Though, since this is a small app, I'll store the whole thing
    // in document.cookie for now as a base64, along with the current
    // user

    document.cookie = Buffer.from(
        JSON.stringify({
            token,
            username,
        }),
        "utf-8"
    ).toString("base64");
}

export function readCredentials(): { token: string; username: string } {
    return JSON.parse(Buffer.from(document.cookie).toString("ascii"));
}
