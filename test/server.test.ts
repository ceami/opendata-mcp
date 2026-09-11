import assert from "node:assert/strict";
import { once } from "node:events";
import type { AddressInfo } from "node:net";
import test from "node:test";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import { createHttpServer } from "../src/http.js";
import { buildFetchRequest } from "../src/tools/fetch_data.js";

const endpointInfo = {
    path: "/items",
    method: "GET" as const,
    params: [
        { name: "serviceKey", value: "" },
        { name: "query", value: "seoul" },
    ],
    headers: [{ name: "Authorization", prefix: "Bearer", value: "" }],
};

test("fetch_data rejects disguised or unapproved hosts before attaching the service key", () => {
    for (const host of ["attacker.invalid", "apis.data.go.kr.attacker.invalid", "apis.data.go.kr@attacker.invalid"]) {
        assert.throws(
            () => buildFetchRequest({ host, base_path: "/v1" }, endpointInfo, "test-secret", new Set(["apis.data.go.kr"])),
            /not allowed/,
        );
    }
});

test("fetch_data keeps allowed GET requests and service-key injection working", () => {
    const request = buildFetchRequest(
        { host: "apis.data.go.kr", base_path: "/v1" },
        endpointInfo,
        "test-secret",
        new Set(["apis.data.go.kr"]),
    );

    assert.equal(request.url.href, "https://apis.data.go.kr/v1/items?serviceKey=test-secret&query=seoul");
    assert.deepEqual(request.headers, { Authorization: "Bearer test-secret" });
});

test("fetch_data never attaches the service key to redirectable non-standard auth headers", () => {
    const request = buildFetchRequest(
        { host: "apis.data.go.kr", base_path: "/v1" },
        { ...endpointInfo, headers: [{ name: "X-Authorization", prefix: "Bearer", value: "" }] },
        "test-secret",
        new Set(["apis.data.go.kr"]),
    );

    assert.equal(request.redirect, "error");
    assert.deepEqual(request.headers, { "X-Authorization": "" });
});

test("Streamable HTTP serves health and the original three MCP tools", async () => {
    const server = createHttpServer({ allowedHosts: [] });
    server.listen(0, "127.0.0.1");
    await once(server, "listening");

    const { port } = server.address() as AddressInfo;
    const baseUrl = `http://127.0.0.1:${port}`;
    const client = new Client({ name: "opendata-mcp-test", version: "1.0.0" });

    try {
        const health = await fetch(`${baseUrl}/health`);
        assert.equal(health.status, 200);
        assert.deepEqual(await health.json(), { status: "ok" });

        await client.connect(new StreamableHTTPClientTransport(new URL(`${baseUrl}/mcp`)));
        const { tools } = await client.listTools();
        assert.deepEqual(
            tools.map(({ name }) => name).sort(),
            ["fetch_data", "get_std_docs", "search_api"],
        );
    } finally {
        await client.close();
        await new Promise<void>((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
    }
});

test("Streamable HTTP rejects MCP bodies larger than 1 MiB", async () => {
    const server = createHttpServer({ allowedHosts: [] });
    server.listen(0, "127.0.0.1");
    await once(server, "listening");

    const { port } = server.address() as AddressInfo;
    try {
        const response = await fetch(`http://127.0.0.1:${port}/mcp`, {
            method: "POST",
            headers: { "content-type": "application/json", accept: "application/json, text/event-stream" },
            body: "x".repeat(1_048_577),
        });
        assert.equal(response.status, 413);
    } finally {
        await new Promise<void>((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
    }
});
