export async function makeMonadic<T>(
    awaitable: Promise<T> | undefined,
    noLog: boolean = false
): Promise<[T | null, Error | null]> {
    if (!awaitable) return [null, new Error("Awaitable is undefined")];
    try {
        return [await awaitable, null];
    } catch (err) {
        if (!noLog)
            console.error(
                `Caught error ${(err as Error).name}: ${(err as Error).message}`
            );
        return [null, err as Error];
    }
}
