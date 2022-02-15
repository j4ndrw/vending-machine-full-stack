import { readCredentials } from "../auth/auth";
import { apiRoute } from "../env/apiConfig";
import { makeRequest } from "../utility/makeRequest";

export async function getProductsFromUser() {
    const { token, username } = readCredentials();
    return await makeRequest(`${apiRoute}/products/from/${username}`, {
        headers: { "x-access-token": token },
    });
}
