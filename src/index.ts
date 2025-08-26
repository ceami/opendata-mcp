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
import { registerCallOpenApiEndpoint } from "./tools/call_openapi_endpoints.js";
import { registerSearchApi } from "./tools/search_api.js";
import { registerGetStdDocs } from "./tools/get_std_docs.js";

export const configSchema = z.object({
    ODP_SERVICE_KEY: z
        .string()
        .describe("Public data service key for authenticated requests")
        .optional()
});

type ServerConfig = z.infer<typeof configSchema>;

export default function createStatelessServer({ config }: { config: ServerConfig }) {
    const server = new McpServer({
        name: "Open Data MCP",
        version: "1.0.0",
    });
    const apiHost = "mcp.ezrnd.co.kr";
    const serviceKey = config.ODP_SERVICE_KEY;

    registerSearchApi(server, apiHost);
    registerGetStdDocs(server, apiHost);
    registerCallOpenApiEndpoint(server, () => {
        return serviceKey || undefined;
    });

    return server.server;
}
