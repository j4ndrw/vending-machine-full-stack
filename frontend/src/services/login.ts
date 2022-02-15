import { readCredentials, storeCredentials } from "../auth/auth";
import { saveLoginStatus } from "../auth/loginStatus";
import { apiRoute } from "../env/apiConfig";
import { makeRequest } from "../utility/makeRequest";

export async function login(username: string, password: string) {
    const { token } = readCredentials();

    const response = await makeRequest(`${apiRoute}/login`, {
        method: "POST",
        body: {
            username,
            password,
        },
        headers: {
            "x-access-token": token || "",
        },
    });

    storeCredentials(response.data.token, username);
    saveLoginStatus(true);
    return response;
}
