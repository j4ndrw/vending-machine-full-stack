import { apiRoute } from "../env/apiConfig";
import { makeRequest } from "../utility/makeRequest";
import { readCredentials, storeCredentials } from "../auth/auth";

export async function getIdToken() {
    const { token, username } = readCredentials();
    const response = await makeRequest(
        `${apiRoute}/token/refresh/${username}`,
        {
            headers: {
                "x-access-token": token,
            },
        }
    );

    if (response.status === 200)
        storeCredentials(response.data.token, response.data.username);
}
