import { readCredentials } from "../auth/auth";
import { apiRoute } from "../env/apiConfig";
import { makeRequest } from "../utility/makeRequest";

export async function getProduct(productId: number) {
    const { token } = readCredentials();
    return await makeRequest(`${apiRoute}/products/${productId}`, {
        headers: { "x-access-token": token },
        method: "POST",
    });
}
