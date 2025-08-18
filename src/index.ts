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
    const apiHost = "mcp.dev.ezrnd.co.kr";
    const serviceKey = config.ODP_SERVICE_KEY;

    registerSearchApi(server, apiHost);
    registerGetStdDocs(server, apiHost);
    registerCallOpenApiEndpoint(server, () => {
        return serviceKey || undefined;
    });

    return server.server;
}
