import { readCredentials } from "../auth/auth";
import { apiRoute } from "../env/apiConfig";
import { makeRequest } from "../utility/makeRequest";

export async function logout() {
    const { token, username } = readCredentials();
    return await makeRequest(`${apiRoute}/logout`, {
        method: "PUT",
        body: {
            username,
        },
        headers: {
            "x-access-token": token,
        },
    });
}
