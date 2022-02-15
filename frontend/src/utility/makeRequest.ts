import { getIdToken } from "../services/getIdToken";
import { APIResponse } from "../types/api";
import { makeMonadic } from "./makeMonadic";

export async function makeRequest(
    url: string,
    options: Omit<RequestInit, "body"> & {
        body?: RequestInit["body"] | Record<string, any>;
    }
): Promise<APIResponse> {
    const [response, fetchErr] = await (() => {
        if (options.method === "GET") {
            return makeMonadic(fetch(url, options as RequestInit));
        }
        return makeMonadic(
            fetch(url, {
                ...options,
                headers: {
                    ...options.headers,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(options.body),
            })
        );
    })();

    if (fetchErr) {
        throw fetchErr;
    }

    const [data, err] = await makeMonadic(response?.json());
    if (err) {
        throw err;
    }

    if (response?.status === 409) {
        await getIdToken();
        return await makeRequest(url, options);
    }

    return { data, status: response?.status };
}
