import { readCredentials } from "../auth/auth";
import { apiRoute } from "../env/apiConfig";
import { makeRequest } from "../utility/makeRequest";

export async function buy(total: number, productIds: number[]) {
    const { token, username } = readCredentials();
    return await makeRequest(`${apiRoute}/buy`, {
        headers: { "x-access-token": token },
        method: "PUT",
        body: { username, total, product_ids: productIds },
    });
}
