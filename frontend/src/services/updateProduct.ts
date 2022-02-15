import { readCredentials } from "../auth/auth";
import { apiRoute } from "../env/apiConfig";
import { makeRequest } from "../utility/makeRequest";

export async function updateProduct(
    productId: number,
    cost: number,
    productName: string
) {
    const { token, username } = readCredentials();
    return await makeRequest(`${apiRoute}/products/${productId}`, {
        headers: { "x-access-token": token },
        method: "PUT",
        body: {
            username,
            cost,
            product_name: productName,
        },
    });
}
