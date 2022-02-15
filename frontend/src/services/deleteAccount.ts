import { readCredentials } from "../auth/auth";
import { apiRoute } from "../env/apiConfig";
import { makeRequest } from "../utility/makeRequest";

export async function deleteAccount() {
    const { token, username } = readCredentials();
    return await makeRequest(`${apiRoute}/users/${username}`, {
        headers: {
            "x-access-token": token,
        },
        method: "DELETE",
    });
}
