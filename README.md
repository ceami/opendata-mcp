## Open Data MCP
[![smithery badge](https://smithery.ai/badge/@iosif2/opendata-mcp)](https://smithery.ai/server/@iosif2/opendata-mcp)

한국 공공데이터포털(OpenAPI)을 더 쉽게 탐색·호출할 수 있도록 돕는 Model Context Protocol(MCP) 서버입니다. 다음과 같은 MCP 도구를 제공합니다:

- **search_api**: 키워드로 공공데이터 API를 검색
- **get_std_docs**: 검색 결과에서 선택한 `listId` 목록으로 표준 문서(markdown) 병합
- **fetch_data**: 표준 문서/메타데이터를 바탕으로 실제 OpenAPI 엔드포인트 호출

내부적으로 검색/문서 도구는 `mcp.ezrnd.co.kr`(HTTPS) 백엔드를 사용합니다.

### 요구 사항
- Docker 또는 Node.js 최신 LTS
- npm

### 설치
```bash
npm install
```

### 실행(개발)
```bash
npm run dev
```

MCP 엔드포인트는 `http://localhost:8787/mcp`, 상태 확인은 `http://localhost:8787/health`입니다.

### Docker 배포
```bash
docker compose up -d --build
docker compose ps
```

Compose 파일은 프록시 네트워크를 지정하지 않습니다. 컨테이너를 프록시 네트워크에 연결한 뒤 `opendata-mcp:8787`의 `/mcp`로 프록시하세요.
외부 공개 시 인증과 요청 빈도 제한은 리버스 프록시에서 적용하세요. 애플리케이션은 MCP 요청 본문을 1 MiB로 제한합니다.

Smithery에는 공개 Streamable HTTP URL(예: `https://mcp.ezrnd.co.kr/mcp`)을 등록합니다. 기존 `smithery.yaml` 기반 호스팅과 구형 `@smithery/cli` 실행 경로는 사용하지 않습니다.

### 설정
- **PORT**: HTTP 포트. 기본값은 `8787`입니다.
- **MCP_ALLOWED_HOSTS**: MCP 요청에 허용할 `Host` 헤더의 쉼표 구분 목록입니다. 기본값은 `mcp.ezrnd.co.kr`과 로컬 개발 호스트입니다.
- **ODP_ALLOWED_HOSTS**: `fetch_data`가 호출할 수 있는 API 호스트의 쉼표 구분 목록입니다. 기본값은 `apis.data.go.kr,api.odcloud.kr`입니다.
- **x-odp-service-key** 요청 헤더: 공공데이터포털 서비스 키. 서버 공용 환경변수로 저장하지 않고 MCP 요청별로 전달합니다.
  - 파라미터 이름에 `serviceKey`가 포함되어 있으면 자동 주입됩니다.
  - 헤더 이름이 `Authorization`이면 `{Prefix} {키}` 형식으로 자동 주입됩니다.
  - 키와 Authorization 값은 로그에 기록하지 않으며, 허용된 API 호스트에만 전송됩니다.

### 제공 도구 상세

#### search_api
- **설명**: 공공데이터포털에서 키워드로 API 목록을 검색합니다.
- **입력**:
  - `query`: 문자열 배열(공백 없는 키워드, 최대 5개 권장)
  - `page`: 페이지 번호(1부터)
  - `pageSize`: 페이지 크기
- **출력**: 검색 결과(JSON 문자열)

#### get_std_docs
- **설명**: `search_api` 결과에서 선택한 항목들의 `listId` 배열을 받아 표준 문서(markdown)를 합쳐 반환합니다.
- **입력**:
  - `listId`: number[]
- **출력**: 통합된 markdown 문자열

#### fetch_data
- **설명**: OpenAPI 메타데이터를 기반으로 특정 엔드포인트를 호출합니다. 기본 프로토콜은 HTTPS입니다.
- **입력**: `requestData`
  - `baseInfo.host`: 예) `apis.data.go.kr` (프로토콜/슬래시 금지)
  - `baseInfo.base_path`: 예) `/B552015/NpsBplcInfoInqireServiceV2`
  - `endpointInfo.path`: 예) `/getBassInfoSearchV2`
  - `endpointInfo.method`: `GET`
  - `endpointInfo.params`: `[{ name, value }]` 배열. 값이 없으면 제외됩니다.
  - `endpointInfo.headers`: `[{ name, prefix, value }]` 배열. `Authorization`에 서비스키 자동 주입 지원.
- **출력**: 응답 본문(JSON 문자열 또는 텍스트)

### 라이선스
이 저장소의 라이선스는 루트의 `LICENSE` 파일을 참고하세요.
