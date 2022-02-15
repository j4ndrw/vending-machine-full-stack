import { readCredentials } from "../auth/auth";
import { apiRoute } from "../env/apiConfig";
import { makeRequest } from "../utility/makeRequest";

export async function getUsers() {
    const { token } = readCredentials();
    return await makeRequest(`${apiRoute}/users`, {
        headers: {
            "x-access-token": token,
        },
    });
}
