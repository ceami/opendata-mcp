## Open Data MCP
[![smithery badge](https://smithery.ai/badge/@iosif2/opendata-mcp)](https://smithery.ai/server/@iosif2/opendata-mcp)

한국 공공데이터포털(OpenAPI)을 더 쉽게 탐색·호출할 수 있도록 돕는 Model Context Protocol(MCP) 서버입니다. 다음과 같은 MCP 도구를 제공합니다:

- **search_api**: 키워드로 공공데이터 API를 검색
- **get_std_docs**: 검색 결과에서 선택한 `listId` 목록으로 표준 문서(markdown) 병합
- **call_openapi_endpoint**: 표준 문서/메타데이터를 바탕으로 실제 OpenAPI 엔드포인트 호출

내부적으로 검색/문서 도구는 `mcp.dev.ezrnd.co.kr`(HTTPS) 백엔드를 사용합니다.

### 요구 사항
- Node.js ≥ 18.17 (권장: 최신 LTS)
- npm (패키지 매니저)

### 설치
```bash
npm install
npm run typecheck
```

### 실행(개발)
Smithery CLI를 사용해 MCP 개발 서버를 구동할 수 있습니다.

```bash
npm run dev
```

> 참고: `@smithery/cli`가 MCP 호스트 역할을 하며, 필요 시 구성 UI를 통해 `ODP_SERVICE_KEY`를 주입할 수 있습니다.

### 환경변수
- **ODP_SERVICE_KEY**: 공공데이터포털 서비스 키. 일부 API는 쿼리 파라미터 또는 Authorization 헤더로 키 주입이 필요합니다.
  - 파라미터 이름에 `serviceKey`가 포함되어 있으면 자동 주입됩니다.
  - 헤더 이름에 `Authorization`이 포함되어 있으면 `Infuser {키}` 형식으로 자동 주입됩니다.

### 제공 도구 상세

#### search_api
- **설명**: 공공데이터포털에서 키워드로 API 목록을 검색합니다.
- **입력**:
  - `query`: 문자열 배열(공백 없는 키워드, 최대 5개 권장)
  - `page`: 페이지 번호(1부터)
  - `pageSize`: 페이지 크기
- **출력**: 검색 결과(JSON 문자열)

예시 입력:
```json
{
  "query": ["기상", "단기예보"],
  "page": 1,
  "pageSize": 10
}
```

#### get_std_docs
- **설명**: `search_api` 결과에서 선택한 항목들의 `listId` 배열을 받아 표준 문서(markdown)를 합쳐 반환합니다.
- **입력**:
  - `listId`: number[]
- **출력**: 통합된 markdown 문자열

예시 입력:
```json
{
  "listId": [12345, 23456]
}
```

#### call_openapi_endpoint
- **설명**: OpenAPI 메타데이터를 기반으로 특정 엔드포인트를 호출합니다. 기본 프로토콜은 HTTPS입니다.
- **입력**: `requestData`
  - `baseInfo.host`: 예) `apis.data.go.kr` (프로토콜/슬래시 금지)
  - `baseInfo.base_path`: 예) `/B552015/NpsBplcInfoInqireServiceV2`
  - `endpointInfo.path`: 예) `/getBassInfoSearchV2`
  - `endpointInfo.method`: `GET` 또는 `POST`
  - `endpointInfo.params`: `[{ name, value }]` 배열. 값이 없으면 제외됩니다.
  - `endpointInfo.headers`: `[{ name, prefix, value }]` 배열. `Authorization`에 서비스키 자동 주입 지원.
  - `endpointInfo.body`: POST 본문(JSON)
- **출력**: 응답 본문(JSON 문자열 또는 텍스트)

예시 입력:
```json
{
  "requestData": {
    "baseInfo": {
      "host": "apis.data.go.kr",
      "base_path": "/B552015/NpsBplcInfoInqireServiceV2"
    },
    "endpointInfo": {
      "path": "/getBassInfoSearchV2",
      "method": "GET",
      "params": [
        { "name": "serviceKey", "value": "" },
        { "name": "pageNo", "value": "1" },
        { "name": "numOfRows", "value": "10" }
      ],
      "headers": [
        { "name": "Authorization", "prefix": "Infuser", "value": "" }
      ]
    }
  }
}
```

### 트러블슈팅
- IDE에서 `zod` 또는 모듈 해석 오류가 보일 때
  1) 상태바에서 TypeScript 버전 클릭 → “Use Workspace Version” 선택
  2) 명령 팔레트 → “TypeScript: Restart TS server”
  3) 프로젝트 루트를 `/Users/<you>/repos/open-data-mcp`로 열었는지 확인
  4) `tsconfig.json`의 모듈 해석은 `NodeNext` 사용. ESM 경로는 `.js` 확장자로 임포트
  5) 필요 시 `rm -rf node_modules package-lock.json && npm install`

### 라이선스
이 저장소의 라이선스는 루트의 `LICENSE` 파일을 참고하세요.

