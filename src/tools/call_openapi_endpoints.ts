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
import { HeaderSchema, ParamSchema, RequestDataSchema } from "../types.js";
import { z } from "zod";


export function registerCallOpenApiEndpoint(server: McpServer, getServiceKey: () => string | undefined) {
    server.registerTool(
        "call_openapi_endpoint",
        {
            title: "Call OpenAPI Endpoint",
            description: `OpenAPI 메타데이터를 기반으로 특정 엔드포인트를 호출합니다.

사용법 지침:
- baseInfo.host: 호스트만 입력(프로토콜/슬래시 금지), 예: "apis.data.go.kr"
- baseInfo.base_path: 선행 슬래시 필수, 예: "/B552015/NpsBplcInfoInqireServiceV2"
- endpointInfo.path: 선행 슬래시 필수, 예: "/getBassInfoSearchV2"
- endpointInfo.method: "GET" 또는 "POST"
- requestParameters: 실제 요청 파라미터를 모두 여기에 넣으세요. 예: {"serviceKey":"", "pageNo":1}
- requestParameters가 꼭 포함되어야 합니다. 빈 객체나 빈 문자열을 전달하거나 생략하지 마세요.
- 인증키가 파라미터로 요구되면 requestParameters.serviceKey 값을 빈 문자열로 두면 자동 주입됩니다.
- 인증이 헤더로 요구되면 endpointInfo.headers에 {"Authorization":""}를 추가하면 "Infuser {키}"로 주입됩니다.
- 서버 실행 시 ODP_SERVICE_KEY 환경변수를 설정해야 자동 주입이 동작합니다.
- JSON(type=json) 응답이 실패하면 해당 파라미터를 제거하고 XML 기본 응답으로 재시도하십시오.
Example of the requestData:
{
    "baseInfo": {
        "host": "apis.data.go.kr",
        "base_path": "/B552015/NpsBplcInfoInqireServiceV2"
    },
    "endpointInfo": {
        "path": "/getBassInfoSearchV2",
        "method": "GET",
        "params": [ // If the param is not provided, the param is not included in the request
            {
                "name": "serviceKey",
                "value": ""
            }
        ],
        "headers": [ // If the header is not provided, the header is not included in the request
            {
                "name": "Authorization",
                "prefix": "Infuser",
                "value": ""
            }
        ]
    }
}
`,

            inputSchema: { requestData: RequestDataSchema },
        },
        async ({ requestData }: { requestData: z.infer<typeof RequestDataSchema> }) => {
            const serviceKey = getServiceKey();
            const endpointUrl = `https://${requestData.baseInfo.host}${requestData.baseInfo.base_path}${requestData.endpointInfo.path}`;
            const method = requestData.endpointInfo.method.toUpperCase();
            const params: Array<z.infer<typeof ParamSchema>> = requestData.endpointInfo.params || [];
            const headers: Array<z.infer<typeof HeaderSchema>> = requestData.endpointInfo.headers || [];
            for (const param of params) {
                if (param.name.toLowerCase().includes("servicekey")) {
                    if (!serviceKey) {
                        return { content: [{ type: "text", text: "serviceKey is not provided. Please provide serviceKey in the request or in the mcp server run command." }] };
                    }
                    param.value = serviceKey;
                }
            }

            for (const header of headers) {
                if (header.name.toLowerCase().includes("authorization")) {
                    if (!serviceKey) {
                        return { content: [{ type: "text", text: "serviceKey is not provided. Please provide serviceKey in the request or in the mcp server run command." }] };
                    }
                    header.value = `${header.prefix} ${serviceKey}`;
                    break;
                }
            }

            try {
                if (method === "GET") {
                    const queryParams = params.reduce((acc, param) => {
                        if (param.value !== undefined && param.value !== null) acc[param.name] = param.value;
                        return acc;
                    }, {} as Record<string, string>);
                    const qs = buildQuery(queryParams);

                    const headerRecord = headers.reduce((acc, h) => {
                        if (h.value !== undefined && h.value !== null) acc[h.name] = h.value;
                        return acc;
                    }, {} as Record<string, string>);

                    const res = await withTimeout(fetch(`${endpointUrl}?${qs}`, { headers: headerRecord }), 30_000);
                    if (!(res as any).ok) {
                        return { content: [{ type: "text", text: `HTTP error occurred: ${(res as any).status} - ${await (res as any).text()}` }] };
                    }
                    const body = await safeJson(res as any);
                    const isJson = typeof body === "object";
                    return isJson
                        ? { content: [{ type: "text", text: JSON.stringify(body) }] }
                        : { content: [{ type: "text", text: String(body) }] };
                } else if (method === "POST") {
                    const headerRecord = headers.reduce((acc, h) => {
                        if (h.value !== undefined && h.value !== null) acc[h.name] = h.value;
                        return acc;
                    }, {} as Record<string, string>);

                    const res = await withTimeout(
                        fetch(endpointUrl, {
                            method: "POST",
                            headers: { "Content-Type": "application/json", ...headerRecord },
                            body: JSON.stringify(requestData.endpointInfo.body || {}),
                        }),
                        30_000
                    );
                    if (!(res as any).ok) {
                        return { content: [{ type: "text", text: `HTTP error occurred: ${(res as any).status} - ${await (res as any).text()}` }] };
                    }
                    const body = await safeJson(res as any);
                    const isJson = typeof body === "object";
                    return isJson
                        ? { content: [{ type: "text", text: JSON.stringify(body) }] }
                        : { content: [{ type: "text", text: String(body) }] };
                } else {
                    return { content: [{ type: "text", text: "Unsupported HTTP method" }] };
                }
            } catch (e: any) {
                return { content: [{ type: "text", text: `An error occurred while requesting: ${e?.message || e}` }] };
            }
        }
    );
}