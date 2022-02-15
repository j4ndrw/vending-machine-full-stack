import { readCredentials } from "../auth/auth";
import { apiRoute } from "../env/apiConfig";
import { makeRequest } from "../utility/makeRequest";

export async function deposit(amount: number) {
    const { token, username } = readCredentials();
    return await makeRequest(`${apiRoute}/deposit`, {
        headers: { "x-access-token": token },
        method: "PUT",
        body: { username, deposit: amount },
    });
}
