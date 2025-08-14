from open_data_mcp.core.server import mcp


@mcp.prompt()
def call_openapi_endpoint_usage_guide() -> str:
    """
    call_openapi_endpoint 툴의 사용법을 반환합니다.
    """
    return """
        `call_openapi_endpoint` 도구는 제공된 OpenAPI 메타데이터를 기반으로 특정 엔드포인트에 API 요청을 보냅니다.
        이 도구를 사용하려면, API 호출에 필요한 모든 정보를 담은 단일 `request_data` 객체를 인자로 전달해야 합니다.

        **`request_data` 객체 구조:**

        1.  `base_info`: API의 기본 주소 정보 (`host`, `base_path`).
        2.  `endpoint_info`: 엔드포인트의 상세 정보 (`path`, `method`, `params`, `headers`).
        3.  `request_parameters`: 실제 요청에 사용할 매개변수.

        **중요: 인증키 (`serviceKey` 또는 `Authorization`) 처리 지침**

        API가 인증키를 요구하는 경우, LLM은 **인증키의 위치(파라미터 또는 헤더)를 파악하고, 값은 항상 빈 문자열("")로 설정해야 합니다.**
        실제 키 값은 서버가 자동으로 안전하게 주입합니다.

        *   **파라미터에 인증키가 필요한 경우:**
            API 명세(`params`)에 `serviceKey`와 유사한 이름의 파라미터가 있다면, `request_parameters` 객체에 해당 키를 포함시키고 값은 `""`로 설정하십시오.
            예: `"request_parameters": { "serviceKey": "", "pageNo": 1, ... }`

        *   **헤더에 인증키가 필요한 경우:**
            API 명세(`headers`)에 `Authorization`과 같은 인증 헤더가 명시되어 있다면, `endpoint_info.headers` 객체에 해당 헤더를 포함시키고 값은 `""`로 설정하십시오.
            예: `"headers": { "Authorization": "", "Content-Type": "application/json" }`

        LLM은 인증키의 **존재와 위치**만 알려주고, **실제 키 값은 절대 포함해서는 안 됩니다.**
    """
