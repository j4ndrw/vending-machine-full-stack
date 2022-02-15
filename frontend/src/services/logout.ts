import { readCredentials, storeCredentials } from "../auth/auth";
import { saveLoginStatus } from "../auth/loginStatus";
import { apiRoute } from "../env/apiConfig";
import { makeRequest } from "../utility/makeRequest";

export async function logout() {
    const { token, username } = readCredentials();
    const response = await makeRequest(`${apiRoute}/logout`, {
        method: "PUT",
        body: {
            username,
        },
        headers: {
            "x-access-token": token,
        },
    });
    saveLoginStatus(false);
    storeCredentials("", "");

    return response;
}
