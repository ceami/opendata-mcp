import requests
from open_data_mcp.core.server import mcp
from open_data_mcp.core.config import settings
from open_data_mcp.schemas import RequestData


@mcp.tool()
def call_openapi_endpoint(request_data: RequestData) -> dict | str:
    """
        `call_openapi_endpoint` 도구는 제공된 OpenAPI 메타데이터를 기반으로 특정 엔드포인트에 API 요청을 보냅니다.
    이 도구를 사용하려면, API 호출에 필요한 모든 정보를 담은 단일 `request_data` 객체를 인자로 전달해야 합니다.

    RequestData 스키마(키 이름과 케이스에 주의: camelCase):
    1) baseInfo: API 기본 주소 정보
       - host (string): 호스트명만 입력(프로토콜/슬래시 금지). 예: "apis.data.go.kr"
       - basePath (string): 반드시 선행 슬래시 포함. 예: "/1471000/FooService"
    2) endpointInfo: 엔드포인트 상세
       - path (string): 반드시 선행 슬래시 포함. 예: "/getList"
       - method (string): 대문자 HTTP 메서드. 예: "GET", "POST"
       - params (array, optional): 엔드포인트의 메타데이터 설명 용도. 실제 요청 값은 여기에 넣지 않음. 필요 없으면 [].
       - headers (object|null, optional): 헤더 메타데이터. 인증 헤더가 요구되면 빈 값으로 키를 추가. 예: {"Authorization": "" }
       - body (object|null, optional): 바디 메타데이터(선택).
    3) requestParameters: 실제 요청에 사용할 매개변수(쿼리/바디 값 포함)
       - 모든 실제 파라미터는 여기에 넣음. 예: {"serviceKey": "", "pageNo": 1, "numOfRows": 10}

    인증키 처리 지침(중요):
    - 인증키가 파라미터로 요구되면 `requestParameters`에 키를 추가하고 값은 항상 빈 문자열("")로 설정합니다.
      예: "requestParameters": { "serviceKey": "", "pageNo": 1 }
    - 인증키가 헤더로 요구되면 `endpointInfo.headers`에 해당 헤더 키를 추가하고 값은 빈 문자열("")로 설정합니다.
      예: "headers": { "Authorization": "" }
    - 실제 키 값은 서버가 자동 주입합니다. 응답에 "SERVICE_KEY_IS_NOT_REGISTERED_ERROR"가 포함되면 활용신청을 진행하세요.
    - 실제 키 값은 서버가 자동 주입합니다. 응답에 "SERVICE_ACCESS_DENIED_ERROR"가 포함되면 활용신청을 진행하세요.
    - 인증 키 값을 mcp 서버 실행시에 --service-key 옵션으로 전달하지 않았다면 이 도구에서는 serviceKey가 파라미터를 통해 요구되면 오류를 발생 시킵니다.
    - 사용자에게 mcp server 실행시에 --service-key 옵션으로 전달하도록 안내하세요.

    호출 실패를 줄이기 위한 권장사항:
    - basePath와 path는 모두 선행 슬래시(`/`)를 포함해야 하며, host에는 프로토콜이나 슬래시를 넣지 마세요.
    - 실제 요청 값은 절대 `endpointInfo.params`에 넣지 말고 반드시 `requestParameters`에 넣으세요.
    - 일부 API는 문서상 JSON을 지원해도 `type=json`에서 서비스 오류가 발생할 수 있습니다.
      - 이 경우 `type` 파라미터를 제거(기본 XML)하여 재시도하세요.
    - 응답이 APPLICATION_ERROR/SERVICE ERROR인 경우:
      - 불필요한 파라미터 제거 후 최소 파라미터(pageNo/numOfRows 등)만으로 재시도
      - 응답 형식 지정(`type=json`)을 제거하여 기본(XML)로 재시도

    예시(식품의약품안전처_식품 이력 정보 `/getPrductInfoList03`):
    {
      "baseInfo": {
        "host": "apis.data.go.kr",
        "basePath": "/1471000/FoodHistInfoService03"
      },
      "endpointInfo": {
        "path": "/getPrductInfoList03",
        "method": "GET",
        "params": [],
        "headers": { "Authorization": "" }
      },
      "requestParameters": {
        "serviceKey": "",
        "pageNo": 1,
        "numOfRows": 10
        // 참고: JSON이 실패할 수 있으므로 "type"은 우선 생략하고 기본(XML)로 호출 권장
        // 필요 시 "type": "json" 추가 후 재시도
      }
    }



        Args:
            request_data (RequestData): An object containing all necessary information for the API call.

        Returns:
            - dict: API의 응답(문자열 XML 또는 JSON). "SERVICE_KEY_IS_NOT_REGISTERED_ERROR"가 포함되면 활용신청 안내가 필요합니다.
    """

    # Properly construct the full URL: host + base_path + path
    endpoint_url = f"http://{request_data.base_info.host}{request_data.base_info.base_path}{request_data.endpoint_info.path}"

    params = request_data.request_parameters.copy()
    headers = request_data.endpoint_info.headers or {}

    # --- Service Key Injection Logic ---
    # 1. Check for serviceKey in query parameters
    for key, value in params.items():
        if "servicekey" in key.lower():
            if settings.service_key is None:
                return {
                    "error": "serviceKey is not provided. Please provide serviceKey in the request or in the mcp server run command."
                }
            params[key] = settings.service_key
            break

    # 2. Check for serviceKey in headers (e.g., Authorization)
    if headers:
        for key in list(headers.keys()):
            if "authorization" in key.lower():
                # Assuming the key format is 'Infuser {key}' as is common in the platform
                if settings.service_key is None:
                    return {
                        "error": "serviceKey is not provided. Please provide serviceKey in the request or in the mcp server run command."
                    }
                headers[key] = f"Infuser {settings.service_key}"
                break
    # --- End of Injection Logic ---

    try:
        method = request_data.endpoint_info.method.upper()

        # Set default headers
        default_headers = {}
        if headers:
            default_headers.update(headers)

        if method == "GET":
            response = requests.get(
                endpoint_url,
                params=params,
                headers=default_headers,
                timeout=30,
                verify=False,
            )
        elif method == "POST":
            response = requests.post(
                endpoint_url,
                json=request_data.endpoint_info.body,
                headers=default_headers,
                timeout=30,
                verify=False,
            )
        else:
            return {"error": "Unsupported HTTP method"}

        response.raise_for_status()
        try:
            return response.json()
        except Exception as e:
            return response.text

    except requests.exceptions.HTTPError as e:
        return {
            "error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while requesting: {e}"}
