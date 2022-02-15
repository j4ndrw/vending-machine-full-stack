import { readCredentials } from "../auth/auth";
import { apiRoute } from "../env/apiConfig";
import { makeRequest } from "../utility/makeRequest";

export async function getProducts() {
    const { token } = readCredentials();
    return await makeRequest(`${apiRoute}/products`, {
        headers: { "x-access-token": token },
        method: "GET",
    });
}
