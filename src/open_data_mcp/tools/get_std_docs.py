from open_data_mcp.common.api_client import ODAPIClient
from open_data_mcp.core.server import mcp
from open_data_mcp.schemas import StdDocsInfo


@mcp.tool()
def get_std_docs(list_id: list[int]) -> str:
    """
    이 MCP 서버의 'get_std_docs' 도구는 사용자가 원하는 데이터를 이전 단계의 search_api 툴에서 반환된 데이터에 대한 표준 문서 요청 도구입니다.
    표준 문서는 다음과 같은 형식으로 반환됩니다.
    [예시]
    ==================================================
    OPENAPI METADATA | 국민연금공단_장애연금심사현황_20161027
    ===================================================
    TITLE: 국민연금공단_장애연금심사현황
    TITLE_EN: National Pension Service_Disability Pension Review Status_20161027
    DESCRIPTION: 국민연금 장애연금심사에 대한 장애유형별 장애등급 결정 현황을 제공하는 API입니다. 이 API는 국민연금 지사 정보 등을 기준으로 지사별 장애연금심사 현황을 조사하는 장애연금심사 정보조회 서비스입니다.
    ORGANIZATION: 국민연금공단
    DEPARTMENT: 디지털전략실 빅데이터부
    CATEGORY: 사회복지 > 공적연금
    FORMAT: JSON+XML
    CREATED AT: 2016-11-02
    PUBLISHED AT: 2023-11-16
    UPDATE AT: 2025-04-30
    PRICING: 무료
    LICENSE: 이용허락범위 제한 없음
    USE PERMISSON ENUNCIATION: 권리이용허가 미포함
    KEYWORDS: 국민연금, 급여, 심사
    OWNERSHIP GROUNDS:
    REGISTER_STATUS: 변경승인
    LIST ID: 3047333
    SOURCE: https://www.data.go.kr/catalog/3047333/openapi.json
    HOST_URL: apis.data.go.kr
    BASE_PATH: B552015/NpsLsnAnntyJgmtInfoInqireServiceV2

    ==================================================
    ENDPOINT INFO | 3047333_EP_/getJgmtSttusInfoSearchV2
    ==================================================
    TITLE: 장애연금 심사현황 조회
    DESCRIPTION: 장애연금 심사현황을 조회하는 API로, 사용자는 특정 기간과 지사코드를 기준으로 장애연금 심사 결과를 확인할 수 있습니다. 이 API는 장애유형별 장애등급 결정 현황을 제공합니다.
    PATH: /getJgmtSttusInfoSearchV2
    METHOD: GET
    REQUEST:
     - HEADERS: None
     - PARAMS:
       - NAME: startDataCrtYm
         - DESCRIPTION: 응답 메시지의 자료생성년월 기준 (예: 202301)
         - TYPE: string
         - REQUIRED: true
       - NAME: endDataCrtYm
         - DESCRIPTION: 응답 메시지의 자료생성년월 기준 (예: 202301)
         - TYPE: string
         - REQUIRED: false
       - NAME: jgmtAcptBrofCd
         - DESCRIPTION: 심사접수지사코드 (예: 001)
         - TYPE: string
         - REQUIRED: false
       - NAME: pageNo
         - DESCRIPTION: 페이지 번호 (기본값: 1)
         - TYPE: string
         - REQUIRED: false
       - NAME: numOfRows
         - DESCRIPTION: 한 페이지 결과 수 (기본값: 10)
         - TYPE: string
         - REQUIRED: false
       - NAME: serviceKey
         - DESCRIPTION: 공공데이터포털에서 발급받은 인증키
         - TYPE: string
         - REQUIRED: true
       - NAME: dataType
         - DESCRIPTION: 응답자료형식 (예: json, xml)
         - TYPE: string
         - REQUIRED: false
     - BODY: None
    RESPONSE:
    CODE: 200
     - DATA SCHEMA
       - response (object):
         - header (object): 결과 메세지 및 코드
           - resultCode (string): 결과코드
           - resultMsg (string): 결과메세지
         - body (object): 응답 본문
           - numOfRows (integer): 한 페이지 결과 수
           - items (object): 심사현황 항목
             - item (array): 심사현황 리스트
               - lsnOgrdCnt (string): 등급외인원수
               - lsnQlfcLackCnt (string): 자격미달인원수
               - casRsltRltnCnt (string): 인과관계인원수
               - dataCrtYm (string): 자료생성년월
               - jgmtAcptBrofCd (string): 심사접수지사코드
               - lsnCnfmMpsbCnt (string): 확인불가인원수
               - lsnDg1Cnt (string): 1급인원수
               - lsnDg2Cnt (string): 2급인원수
               - lsnDg3Cnt (string): 3급인원수
               - lsnDg4Cnt (string): 4급인원수
               - lsnNdcdCnt (string): 결정보류인원수
           - totalCount (integer): 전체 결과 수
           - pageNo (integer): 페이지 번호

    EXAMPLE USAGE:
    bash 명령어 예시:
    curl -X GET "https://apis.data.go.kr/B552015/NpsLsnAnntyJgmtInfoInqireServiceV2/getJgmtSttusInfoSearchV2?startDataCrtYm=202301&numOfRows=10&pageNo=1" -H "Authorization: Infuser {YOUR_API_KEY}"

    python 코드 예시:
    import requests

    url = "https://apis.data.go.kr/B552015/NpsLsnAnntyJgmtInfoInqireServiceV2/getJgmtSttusInfoSearchV2"
    headers = {
        "Authorization": "Infuser {YOUR_API_KEY}"
    }
    params = {
        "startDataCrtYm": "202301",
        "numOfRows": 10,
        "pageNo": 1
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    print(data)

    markdown 필드의 데이터가 표준 문서로 다음과 같은 정보를 담고 있습니다.
    데이터의 형식, 요청 방법, 응답 형식, 예시 사용법 등을 포함하고 있습니다.
    이 데이터를 통해 사용자가 원하는 데이터를 찾을 수 있습니다.
    사용자가 원하는 데이터를 찾기 위해서는 다음과 같은 절차를 따라야 합니다.
    1. 사용자가 원하는 데이터의 키워드를 입력합니다.
    2. 입력된 키워드를 통해 search_api 툴을 통해 데이터를 검색합니다.
    3. 검색된 데이터 중 하나를 선택합니다.
    4. 선택된 데이터를 통해 get_std_docs 툴을 통해 표준 문서를 요청합니다.
    ** 절대로 임의 병렬 도구 호출을 진행하지 말고 리스트 형태로 list_id 파라미터를 전달하세요. **

    Args:
        list_id (int): The list ID of the data to get the standard document for.

    Returns:
        str: A standard document for the given list ID.
    """
    client = ODAPIClient()
    std_docs = client.get_std_docs(list_id=list_id)
    return "\n".join([doc.markdown for doc in std_docs])
