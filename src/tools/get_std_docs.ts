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
import { z } from "zod";
import { withTimeout } from "../utils.js";
import { getStdDocsInputSchema, StdDocsInfoSchema } from "../types.js";
import { logger } from "../logger.js";


export function registerGetStdDocsTool(server: McpServer, apiHost: string) {
    server.registerTool(
        "get_std_docs",
        {
            title: "Get Standard Documents",
            description: `Get standard documents from the search results.`,
            inputSchema: getStdDocsInputSchema,
        },
        async ({ listId }: { listId: number[] }) => {
            logger.info(`Getting standard documents from ${apiHost} with listId: ${listId}`);
            const baseUrl = `https://${apiHost}/api/v1/document/std-docs`;
            const usp = new URLSearchParams();
            for (const id of listId) usp.append("list_ids", String(id));
            usp.append("page", "1");
            usp.append("page_size", String(listId.length));

            const res = await withTimeout(fetch(`${baseUrl}?${usp.toString()}`), 30_000);
            if (!(res as any).ok) {
                const text = await (res as any).text();
                logger.error(`HTTP error occurred: ${(res as any).status} - ${text}`);
                return { content: [{ type: "text", text: `HTTP error occurred: ${(res as any).status} - ${text}` }] };
            }
            const docs = await (res as any).json();
            logger.info(`Standard documents: ${JSON.stringify(docs)}`);
            const parsed = z.array(StdDocsInfoSchema).safeParse(docs);
            const joined = parsed.success
                ? parsed.data.map((d: z.infer<typeof StdDocsInfoSchema>) => d.markdown).join("\n")
                : Array.isArray(docs)
                    ? (docs as any[]).map((d: any) => d?.markdown ?? "").join("\n")
                    : String(docs);
            logger.info(`Standard documents joined: ${joined}`);
            return { content: [{ type: "text", text: joined }] };
        }
    );
}