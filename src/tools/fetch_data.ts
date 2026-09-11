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
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { buildQuery, safeJson } from "../utils.js";
import { FetchDataInputSchema, BaseInfoSchema, EndpointInfoSchema } from "../types.js";
import { z } from "zod";
import { logger } from "../logger.js";

type BaseInfo = z.infer<typeof BaseInfoSchema>;
type EndpointInfo = z.infer<typeof EndpointInfoSchema>;

const DEFAULT_ALLOWED_API_HOSTS = ["apis.data.go.kr", "api.odcloud.kr"];

function getAllowedApiHosts() {
    return new Set(
        (process.env.ODP_ALLOWED_HOSTS?.split(",") ?? DEFAULT_ALLOWED_API_HOSTS)
            .map((host) => host.trim().toLowerCase())
            .filter(Boolean),
    );
}

export function buildFetchRequest(
    baseInfo: BaseInfo,
    endpointInfo: EndpointInfo,
    serviceKey: string | undefined,
    allowedHosts: ReadonlySet<string>,
) {
    const host = baseInfo.host.trim().toLowerCase();
    if (!allowedHosts.has(host)) {
        throw new Error(`API host is not allowed: ${host}`);
    }
    if (!baseInfo.base_path.startsWith("/") || !endpointInfo.path.startsWith("/")) {
        throw new Error("API paths must start with '/'");
    }

    const url = new URL(`https://${host}`);
    url.pathname = `${baseInfo.base_path.replace(/\/$/, "")}${endpointInfo.path}`;
    const queryParams = Object.fromEntries(
        (endpointInfo.params ?? [])
            .map((param) => [
                param.name,
                param.name.toLowerCase().includes("servicekey") ? serviceKey : param.value,
            ])
            .filter((entry): entry is [string, string] => entry[1] !== undefined && entry[1] !== null),
    );
    url.search = buildQuery(queryParams);

    let authorizationInjected = false;
    const headers = Object.fromEntries(
        (endpointInfo.headers ?? []).map((header) => {
            if (!authorizationInjected && serviceKey && header.name.toLowerCase() === "authorization") {
                authorizationInjected = true;
                return [header.name, `${header.prefix} ${serviceKey}`];
            }
            return [header.name, header.value];
        }),
    );

    return { url, headers, redirect: "error" as const };
}

export function registerFetchDataTool(
    server: McpServer,
    getServiceKey: () => string | undefined,
    allowedHosts = getAllowedApiHosts(),
) {
    server.registerTool(
        "fetch_data",
        {
            title: "Fetch Data",
            description: `Fetch data from the API.(Base on information of get_std_docs tool)`,
            inputSchema: FetchDataInputSchema
        },
        async ({ baseInfo, endpointInfo }: { baseInfo: BaseInfo, endpointInfo: EndpointInfo }) => {
            logger.info(`Fetching data from ${baseInfo.host}${baseInfo.base_path}${endpointInfo.path}`);
            const serviceKey = getServiceKey();

            try {
                const request = buildFetchRequest(baseInfo, endpointInfo, serviceKey, allowedHosts);
                const res = await fetch(request.url, {
                    headers: request.headers,
                    redirect: request.redirect,
                    signal: AbortSignal.timeout(30_000),
                });
                if (!res.ok) {
                    logger.error(`HTTP error occurred: ${res.status}`);
                    return { content: [{ type: "text", text: `HTTP error occurred: ${res.status}` }] };
                }
                const body = await safeJson(res);
                return typeof body === "object"
                    ? { content: [{ type: "text", text: JSON.stringify(body) }] }
                    : { content: [{ type: "text", text: String(body) }] };
            } catch (e: any) {
                let message = e?.message || String(e);
                if (serviceKey) {
                    message = message.replaceAll(serviceKey, "[REDACTED]").replaceAll(encodeURIComponent(serviceKey), "[REDACTED]");
                }
                logger.error(`An error occurred while requesting: ${message}`);
                return { content: [{ type: "text", text: `An error occurred while requesting: ${message}` }] };
            }
        }
    );
}
