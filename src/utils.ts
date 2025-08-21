/*
 * Copyright 2025 Team Aeris
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
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