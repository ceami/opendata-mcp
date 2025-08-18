import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { withTimeout } from "../utils.js";
import { StdDocsInfoSchema } from "../types.js";


export function registerGetStdDocs(server: McpServer, apiHost: string) {
    server.registerTool(
        "get_std_docs",
        {
            title: "Get Standard Documents",
            description: `검색 결과에서 선택한 데이터들의 listId 배열을 받아 표준 문서(markdown)를 합쳐 반환합니다.

사용법 지침:
- listId: search_api 결과에서 선택한 항목들의 listId 배열(여러 개 가능)
- 병렬 호출 금지. 하나의 호출에 배열로 전달
- 반환 markdown에는 엔드포인트, 파라미터, 예시 사용법이 포함됩니다.
- 반환 문서를 검토 후 call_openapi_endpoint에 필요한 파라미터를 구성하세요.`,
            inputSchema: { listId: z.array(z.number().describe("search_api 결과의 listId")) },
        },
        async ({ listId }: { listId: number[] }) => {
            const baseUrl = `https://${apiHost}/api/v1/document/std-docs`;
            const usp = new URLSearchParams();
            for (const id of listId) usp.append("list_ids", String(id));
            usp.append("page", "1");
            usp.append("page_size", String(listId.length));

            const res = await withTimeout(fetch(`${baseUrl}?${usp.toString()}`), 30_000);
            if (!(res as any).ok) {
                const text = await (res as any).text();
                return { content: [{ type: "text", text: `HTTP error occurred: ${(res as any).status} - ${text}` }] };
            }
            const docs = await (res as any).json();
            const parsed = z.array(StdDocsInfoSchema).safeParse(docs);
            const joined = parsed.success
                ? parsed.data.map((d: z.infer<typeof StdDocsInfoSchema>) => d.markdown).join("\n")
                : Array.isArray(docs)
                    ? (docs as any[]).map((d: any) => d?.markdown ?? "").join("\n")
                    : String(docs);
            return { content: [{ type: "text", text: joined }] };
        }
    );
}