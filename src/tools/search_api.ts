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
import { withTimeout } from "../utils.js";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { searchApiInputSchema, SearchApiResponseSchema } from "../types.js";
import { logger } from "../logger.js";

export function registerSearchApiTool(server: McpServer, apiHost: string) {
    server.registerTool(
        "search_api",
        {
            title: "Search Open Data APIs",
            description: `Search for APIs in the Open Data Portal using keywords.(API Provider: OpenDataAPI(mcp.ezrnd.co.kr))`,
            inputSchema: searchApiInputSchema,
        },
        async ({ query, page, pageSize }: { query: string[]; page: number; pageSize: number }) => {
            logger.info(`Searching for APIs with query: ${query.join(", ")}`);
            const baseUrl = `https://${apiHost}/api/v1/search/title`;
            const usp = new URLSearchParams();
            for (const q of query) usp.append("query", q);
            usp.append("page", String(page));
            usp.append("page_size", String(pageSize));

            const res = await withTimeout(fetch(`${baseUrl}?${usp.toString()}`), 30_000);
            if (!(res as any).ok) {
                const text = await (res as any).text();
                logger.error(`HTTP error occurred: ${(res as any).status} - ${text}`);
                return { content: [{ type: "text", text: `HTTP error occurred: ${(res as any).status} - ${text}` }] };
            }
            const rawData = await (res as any).json();
            logger.info(`Search API response: ${JSON.stringify(rawData)}`);
            try {
                const parsedData = SearchApiResponseSchema.parse(rawData);

                const formattedResponse = {
                    total: parsedData.total,
                    page: parsedData.page,
                    pageSize: parsedData.pageSize,
                    results: parsedData.results.map(item => ({
                        listId: item.listId,
                        listTitle: item.listTitle,
                        title: item.title,
                        orgNm: item.orgNm,
                        dataType: item.dataType,
                        score: item.score,
                        detail: item.detail ? {
                            title: item.detail.title,
                            description: item.detail.description,
                            endpoint: item.detail.endpoint?.map(ep => ({
                                title: ep.title,
                                description: ep.description
                            }))
                        } : null
                    }))
                };
                return { content: [{ type: "text", text: JSON.stringify(formattedResponse, null, 2) }] };
            } catch (error) {
                logger.error("Failed to parse search API response:", error);
                return { content: [{ type: "text", text: JSON.stringify(rawData, null, 2) }] };
            }
        }
    );
}