import { readCredentials } from "../auth/auth";
import { apiRoute } from "../env/apiConfig";
import { makeRequest } from "../utility/makeRequest";

export async function createProduct(cost: number, productName: string) {
    const { token, username } = readCredentials();
    return await makeRequest(`${apiRoute}/products`, {
        headers: {
            "x-access-token": token,
        },
        method: "POST",
        body: {
            username,
            cost,
            product_name: productName,
        },
    });
}
