const url =
    process.env.NODE_ENV === "development" ? "http://localhost:5000" : "";
export const apiRoute = `${url}/api/vendingmachine`;
