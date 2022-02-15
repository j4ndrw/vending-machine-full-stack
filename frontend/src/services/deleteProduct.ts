import { readCredentials } from "../auth/auth";
import { apiRoute } from "../env/apiConfig";
import { makeRequest } from "../utility/makeRequest";

export async function deleteProduct(productId: number) {
    const { token, username } = readCredentials();
    return await makeRequest(`${apiRoute}/products/${productId}`, {
        headers: { "x-access-token": token },
        method: "DELETE",
        body: { username },
    });
}
