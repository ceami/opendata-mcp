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
import { withTimeout, buildQuery, safeJson } from "../utils.js";
import { HeaderSchema, ParamSchema, FetchDataInputSchema, BaseInfoSchema, EndpointInfoSchema } from "../types.js";
import { z } from "zod";
import { logger } from "../logger.js";


export function registerFetchDataTool(server: McpServer, getServiceKey: () => string | undefined) {
    server.registerTool(
        "fetch_data",
        {
            title: "Fetch Data",
            description: `Fetch data from the API.(Base on information of get_std_docs tool)`,
            inputSchema: FetchDataInputSchema
        },
        async ({ baseInfo, endpointInfo }: { baseInfo: z.infer<typeof BaseInfoSchema>, endpointInfo: z.infer<typeof EndpointInfoSchema> }) => {
            logger.info(`Fetching data from ${baseInfo.host}${baseInfo.base_path}${endpointInfo.path}`);
            const serviceKey = getServiceKey();
            const endpointUrl = `https://${baseInfo.host}${baseInfo.base_path}${endpointInfo.path}`;
            const method = endpointInfo.method.toUpperCase();
            const params: Array<z.infer<typeof ParamSchema>> = endpointInfo.params || [];
            const headers: Array<z.infer<typeof HeaderSchema>> = endpointInfo.headers || [];
            for (const param of params) {
                if (param.name.toLowerCase().includes("servicekey")) {
                    param.value = serviceKey;
                }
            }

            for (const header of headers) {
                if (header.name.toLowerCase().includes("authorization")) {
                    header.value = `${header.prefix} ${serviceKey}`;
                    break;
                }
            }

            try {
                if (method === "GET") {
                    const queryParams = params.reduce((acc, param) => {
                        if (param.value !== undefined && param.value !== null) acc[param.name] = param.value;
                        logger.info(`Query parameter: ${param.name} = ${param.value}`);
                        return acc;
                    }, {} as Record<string, string>);
                    const qs = buildQuery(queryParams);

                    const headerRecord = headers.reduce((acc, h) => {
                        if (h.value !== undefined && h.value !== null) acc[h.name] = h.value;
                        logger.info(`Header: ${h.name} = ${h.value}`);
                        return acc;
                    }, {} as Record<string, string>);

                    const res = await withTimeout(fetch(`${endpointUrl}?${qs}`, { headers: headerRecord }), 30_000);
                    if (!(res as any).ok) {
                        logger.error(`HTTP error occurred: ${(res as any).status}`);
                        return { content: [{ type: "text", text: `HTTP error occurred: ${(res as any).status}` }] };
                    }
                    const body = await safeJson(res as any);
                    const isJson = typeof body === "object";
                    logger.info(`Fetch data response: ${JSON.stringify(body)}`);
                    return isJson
                        ? { content: [{ type: "text", text: JSON.stringify(body) }] }
                        : { content: [{ type: "text", text: String(body) }] };
                } else {
                    logger.error(`Unsupported HTTP method: ${method}`);
                    return { content: [{ type: "text", text: `Unsupported HTTP method: ${method}` }] };
                }
            } catch (e: any) {
                logger.error(`An error occurred while requesting: ${e?.message || e}`);
                return { content: [{ type: "text", text: `An error occurred while requesting: ${e?.message || e}` }] };
            }
        }
    );
}