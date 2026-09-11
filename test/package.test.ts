import assert from "node:assert/strict";
import { mkdtemp, readFile, rm, symlink, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { pathToFileURL } from "node:url";
import { isMainModule } from "../src/http.js";
import test from "node:test";

const packageJsonUrl = new URL("../package.json", import.meta.url);
const httpEntryUrl = new URL("../src/http.ts", import.meta.url);

test("package exposes the local HTTP MCP server through npx", async () => {
  const packageJson = JSON.parse(await readFile(packageJsonUrl, "utf8"));
  const httpEntry = await readFile(httpEntryUrl, "utf8");

  assert.equal(packageJson.name, "@aeriis-kr/opendata-mcp");
  assert.equal(packageJson.version, "1.0.3");
  assert.equal(packageJson.main, "./build/index.js");
  assert.equal(packageJson.module, "./build/index.js");
  assert.deepEqual(packageJson.bin, { "opendata-mcp": "build/http.js" });
  assert.deepEqual(packageJson.files, ["build", "README.md", "LICENSE"]);
  assert.equal(packageJson.scripts.prepack, "npm run build");
  assert.equal(packageJson.publishConfig.access, "public");
  assert.ok(httpEntry.startsWith("#!/usr/bin/env node\n"));
});
test("CLI entrypoint resolves the npm bin symlink", async () => {
  const testDir = await mkdtemp(join(tmpdir(), "opendata-mcp-bin-"));
  const target = join(testDir, "http.js");
  const bin = join(testDir, "opendata-mcp");

  try {
    await writeFile(target, "");
    await symlink(target, bin);
    assert.equal(isMainModule(pathToFileURL(target).href, bin), true);
  } finally {
    await rm(testDir, { recursive: true, force: true });
  }
});
