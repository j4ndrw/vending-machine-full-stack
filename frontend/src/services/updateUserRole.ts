import { readCredentials } from "../auth/auth";
import { apiRoute } from "../env/apiConfig";
import { Role } from "../types/role";
import { makeRequest } from "../utility/makeRequest";

export async function updateUserRole(role: Role) {
    const { token, username } = readCredentials();
    return await makeRequest(`${apiRoute}/users/${username}`, {
        headers: {
            "x-access-token": token,
        },
        method: "PUT",
        body: { role },
    });
}
