import { z } from "zod";
import { withTimeout } from "../utils.js";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { SearchApiResponseSchema } from "../types.js";

export function registerSearchApi(server: McpServer, apiHost: string) {
    server.registerTool(
        "search_api",
        {
            title: "Search Open Data APIs",
            description: `공공데이터포털에서 키워드로 API 목록을 검색합니다.

사용법 지침:
- query: 공백 없는 키워드 문자열 배열(최대 5개 권장)
- page, pageSize: 페이지 번호와 크기
- 사용자가 긴 문장으로 요구하면, 공백 없는 핵심 키워드 최대 5개를 추출해 검색
- 병렬 도구 호출 금지. 반드시 하나의 요청에 키워드 배열을 담아 호출
- 결과 중 가장 적합한 항목의 listId를 이용해 'get_std_docs'로 표준 문서를 요청하세요.`,
            inputSchema: {
                query: z.array(z.string().describe("공백 없는 검색 키워드")).describe("키워드 배열"),
                page: z.number().describe("페이지 번호(1부터)"),
                pageSize: z.number().describe("페이지 크기"),
            },
        },
        async ({ query, page, pageSize }: { query: string[]; page: number; pageSize: number }) => {
            const baseUrl = `https://${apiHost}/api/v1/search/title`;
            const usp = new URLSearchParams();
            for (const q of query) usp.append("query", q);
            usp.append("page", String(page));
            usp.append("page_size", String(pageSize));

            const res = await withTimeout(fetch(`${baseUrl}?${usp.toString()}`), 30_000);
            if (!(res as any).ok) {
                const text = await (res as any).text();
                return { content: [{ type: "text", text: `HTTP error occurred: ${(res as any).status} - ${text}` }] };
            }
            const rawData = await (res as any).json();

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
                console.error("Failed to parse search API response:", error);
                return { content: [{ type: "text", text: JSON.stringify(rawData, null, 2) }] };
            }
        }
    );
}