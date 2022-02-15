export interface APIResponse {
    data: {
        message: string;
        status: number;
        [k: string]: any;
    };
    status?: number;
}
