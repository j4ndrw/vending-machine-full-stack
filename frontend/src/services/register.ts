import { apiRoute } from "../env/apiConfig";
import { Role } from "../types/role";
import { makeRequest } from "../utility/makeRequest";

export async function register(username: string, password: string, role: Role) {
    return await makeRequest(`${apiRoute}/register`, {
        method: "POST",
        body: {
            username,
            password,
            role,
        },
    });
}
