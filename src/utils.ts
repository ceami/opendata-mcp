
export function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
    return new Promise<T>((resolve, reject) => {
        const id = setTimeout(() => reject(new Error("Request timeout")), ms);
        promise
            .then((v) => {
                clearTimeout(id);
                resolve(v);
            })
            .catch((e) => {
                clearTimeout(id);
                reject(e);
            });
    });
}

export function buildQuery(params: Record<string, unknown>): string {
    const usp = new URLSearchParams();
    for (const [key, value] of Object.entries(params)) {
        if (Array.isArray(value)) {
            for (const v of value) {
                usp.append(key, String(v));
            }
        } else if (value !== undefined && value !== null) {
            usp.append(key, String(value));
        }
    }
    return usp.toString();
}
export async function safeJson(res: Response | globalThis.Response): Promise<any | string> {
    const response = res as globalThis.Response;
    const rawText = await response.text();
    const trimmed = rawText.trim();
    if (trimmed.length === 0) return "";
    try {
        const contentType = response.headers?.get?.("content-type") ?? "";
        if (
            contentType.includes("application/json") ||
            contentType.includes("+json") ||
            trimmed.startsWith("{") ||
            trimmed.startsWith("[")
        ) {
            return JSON.parse(rawText);
        }
    } catch {
        // fall through and return raw text
    }
    return rawText;
}