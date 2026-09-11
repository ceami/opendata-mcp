#!/usr/bin/env node

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
import { realpathSync } from "node:fs";
import { createServer, type IncomingMessage, type ServerResponse } from "node:http";
import { pathToFileURL } from "node:url";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import createStatelessServer from "./index.js";
import { logger } from "./logger.js";

function envList(name: string, fallback: string[]) {
    return (process.env[name]?.split(",") ?? fallback).map((value) => value.trim()).filter(Boolean);
}

const MAX_BODY_BYTES = 1024 * 1024;
const BODY_TOO_LARGE = Symbol("body-too-large");
const defaultPort = process.env.PORT ?? "8787";

function readJsonBody(req: IncomingMessage): Promise<unknown | typeof BODY_TOO_LARGE> {
    return new Promise((resolve, reject) => {
        const chunks: Buffer[] = [];
        let size = 0;
        let finished = false;

        req.on("data", (chunk: Buffer) => {
            if (finished) return;
            size += chunk.length;
            if (size > MAX_BODY_BYTES) {
                finished = true;
                chunks.length = 0;
                resolve(BODY_TOO_LARGE);
                return;
            }
            chunks.push(chunk);
        });
        req.once("end", () => {
            if (finished) return;
            finished = true;
            try {
                resolve(JSON.parse(Buffer.concat(chunks).toString("utf8")));
            } catch (error) {
                reject(error);
            }
        });
        req.once("error", reject);
    });
}

function writeJsonRpcError(res: ServerResponse, status: number, code: number, message: string) {
    res.writeHead(status, { "content-type": "application/json" }).end(JSON.stringify({
        jsonrpc: "2.0",
        error: { code, message },
        id: null,
    }));
}

export function createHttpServer({
    allowedHosts = envList("MCP_ALLOWED_HOSTS", ["mcp.ezrnd.co.kr", `localhost:${defaultPort}`, `127.0.0.1:${defaultPort}`]),
} = {}) {
    const httpServer = createServer(async (req, res) => {
        const pathname = new URL(req.url ?? "/", "http://localhost").pathname;

        if (req.method === "GET" && pathname === "/health") {
            res.writeHead(200, { "content-type": "application/json" }).end(JSON.stringify({ status: "ok" }));
            return;
        }
        if (pathname !== "/mcp") {
            res.writeHead(404).end();
            return;
        }

        let body: unknown;
        if (req.method === "POST") {
            try {
                body = await readJsonBody(req);
            } catch {
                writeJsonRpcError(res, 400, -32700, "Parse error");
                return;
            }
            if (body === BODY_TOO_LARGE) {
                writeJsonRpcError(res, 413, -32000, "Request body too large");
                return;
            }
        }

        const header = req.headers["x-odp-service-key"];
        const serviceKey = Array.isArray(header) ? header[0] : header;
        const mcpServer = createStatelessServer({ config: { ODP_SERVICE_KEY: serviceKey } });
        const transport = new StreamableHTTPServerTransport({
            sessionIdGenerator: undefined,
            enableDnsRebindingProtection: true,
            allowedHosts,
        });
        res.once("close", () => {
            void Promise.allSettled([transport.close(), mcpServer.close()]);
        });

        try {
            await mcpServer.connect(transport);
            await transport.handleRequest(req, res, body);
        } catch (error) {
            logger.error(`MCP request failed: ${error instanceof Error ? error.message : String(error)}`);
            if (!res.headersSent) {
                writeJsonRpcError(res, 500, -32603, "Internal server error");
            }
        }
    });
    httpServer.requestTimeout = 30_000;
    httpServer.headersTimeout = 10_000;
    return httpServer;
}

export function isMainModule(moduleUrl: string, entryPath: string | undefined) {
    return entryPath !== undefined && moduleUrl === pathToFileURL(realpathSync(entryPath)).href;
}

if (isMainModule(import.meta.url, process.argv[1])) {
    const port = Number(process.env.PORT ?? 8787);
    if (!Number.isInteger(port) || port < 1 || port > 65535) {
        throw new Error("PORT must be an integer between 1 and 65535");
    }

    const server = createHttpServer();
    server.listen(port, "0.0.0.0", () => logger.info(`Open Data MCP listening on 0.0.0.0:${port}/mcp`));
    for (const signal of ["SIGINT", "SIGTERM"] as const) {
        process.once(signal, () => server.close(() => process.exit(0)));
    }
}
