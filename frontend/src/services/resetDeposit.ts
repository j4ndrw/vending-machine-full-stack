import { readCredentials } from "../auth/auth";
import { apiRoute } from "../env/apiConfig";
import { makeRequest } from "../utility/makeRequest";

export async function resetDeposit() {
    const { token, username } = readCredentials();
    return await makeRequest(`${apiRoute}/deposit/reset`, {
        headers: { "x-access-token": token },
        method: "PUT",
        body: { username },
    });
}
