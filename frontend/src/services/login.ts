import { storeCredentials } from "../auth/auth";
import { apiRoute } from "../env/apiConfig";
import { makeRequest } from "../utility/makeRequest";

export async function login(username: string, password: string) {
    const response = await makeRequest(`${apiRoute}/login`, {
        method: "POST",
        body: {
            username,
            password,
        },
    });

    storeCredentials(response.data.token, username);
}
