from open_data_mcp.core.server import mcp


@mcp.prompt()
def get_std_docs_usage_guide():
    """
    get_std_docs 툴의 사용법을 반환합니다.
    """
    return """
        이 MCP 서버의 'get_std_docs' 도구는 사용자가 원하는 데이터를 이전 단계의 search_api 툴에서 반환된 데이터 중 하나를 선택하여 표준 문서를 요청하기 위한 도구입니다.
        표준 문서는 다음과 같은 형식으로 반환됩니다.
        [예시]
        {
            "id": "uddi:bc34aa8d-cb7d-4ee3-a21c-ccd622de0031_202208111515",
            "list_id": 15103306,
            "title": "전라북도_아동 급식카드 가맹점 정보_20220427",
            "description": "전북특별자치도 아동급식카드 가맹점 정보는 결식 우려 아동에게 발급되는 아동급식카드를 사용할 수 있는 가맹점들의 현황을 제공하는 데이터입니다. 이 데이터는 아동들이 건강하고 행복하게 성장할 수 있도록 급식을 효율적으로 제공하기 위한 목적으로 구축되었습니다.\r\n이 데이터의 항목은 가맹점명, 소재지도로명주소 등을 기준으로 전라북도 아동복지급식카드 가맹점을 조회하는 아동 급식 카드 가맹점 조회 서비스로 구성되었으며,\r\n이를 통해 아동들이 근처에서 아동급식카드를 사용할 수 있는 식당이나 편의점 등을 쉽게 찾을 수 있도록 관련 정책수립 및 분석에도 활용될 수 있습니다",
            "detail_url": "https://www.data.go.kr/data/15103306/openapi.do",
            "markdown": '```markdown\n==================================================\nOPENAPI METADATA | 전라북도_아동 급식카드 가맹점 정보_20220427\n==================================================\n\nTITLE: 전라북도_아동 급식카드 가맹점 정보_20220427\nTITLE_EN: Jeollabuk-do_Children\'s Meal Card Merchant Information_20220427\nDESCRIPTION: 전북특별자치도 아동급식카드 가맹점 정보는 결식 우려 아동에게 발급되는 아동급식카드를 사용할 수 있는 가맹점들의 현황을 제공하는 데이터입니다. 이 데이터는 아동들이 건강하고 행복하게 성장할 수 있도록 급식을 효율적으로 제공하기 위한 목적으로 구축되었습니다. 이 데이터의 항목은 가맹점명, 소재지도로명주소 등을 기준으로 전라북도 아동복지급식카드 가맹점을 조회하는 아동 급식 카드 가맹점 조회 서비스로 구성되었으며, 이를 통해 아동들이 근처에서 아동급식카드를 사용할 수 있는 식당이나 편의점 등을 쉽게 찾을 수 있도록 관련 정책수립 및 분석에도 활용될 수 있습니다.\nORGANIZATION: 전북특별자치도\nDEPARTMENT: 디지털산업과\nCATEGORY: 사회복지 > 취약계층지원\nFORMAT: XML\nCREATED AT: 2022-08-05\nPUBLISHED AT: 2022-08-05\nUPDATE AT: 2025-06-19\nPRICING: 무료\nLICENSE: 이용허락범위 제한 없음\nUSE PERMISSON ENUNCIATION: 권리이용허가 미포함\nKEYWORDS: 아동, 급식, 가맹점, 아동급식카드, 소재지, 업종, 아동복지, 결식아동\nOWNERSHIP GROUNDS:\nREGISTER_STATUS: 등록승인\nLIST ID: 15103306\nSOURCE: https://www.data.go.kr/data/15103306/openapi.do\nHOST_URL: apis.data.go.kr\nBASE_PATH: 6450000/childfoodcard\n\n==================================================\nENDPOINT INFO | 15103306_EP_/getChildWelfareCardList\n==================================================\n\nTITLE: 아동 급식카드 가맹점 목록 조회\nDESCRIPTION: 아동 급식카드 가맹점 목록을 조회하는 API입니다. 이 API를 통해 결식 우려 아동이 사용할 수 있는 가맹점의 정보를 제공합니다. 사용자는 가맹점명, 소재지도로명주소 등을 기준으로 가맹점을 검색할 수 있습니다.\nPATH: /getChildWelfareCardList\nMETHOD: GET\nREQUEST:\n - HEADERS:\n - PARAMS:\n   - NAME: serviceKey\n     - DESCRIPTION: 공공데이터포털에서 받은 인증키\n     - TYPE: string\n     - REQUIRED: true\n   - NAME: pageNo\n     - DESCRIPTION: 페이지번호\n     - TYPE: string\n     - REQUIRED: true\n   - NAME: numOfRows\n     - DESCRIPTION: 한 페이지 결과 수\n     - TYPE: string\n     - REQUIRED: true\n   - NAME: mrhstNm\n     - DESCRIPTION: 가맹점명\n     - TYPE: string\n     - REQUIRED: false\n - BODY:\nRESPONSE:\nCODE: 200\n - DATA SCHEMA\n   - response (object):\n     - header (object): header\n       - resultCode (string): 결과코드\n       - resultMsg (string): 결과메세지\n     - body (object): body\n       - numOfRows (number): 한 페이지의 결과 수\n       - pageNo (number): 페이지 번호\n       - totalCount (number): 전체 결과 수\n       - data (array): 가맹점 정보 목록\n         - item (object): 가맹점 정보\n           - mrhstNm (string): 가맹점명\n           - rdnmadr (string): 소재지도로명주소\n           - phoneNumber (string): 전화번호\n           - institutionNm (string): 관리기관명\n           - institutionPhoneNumber (string): 관리기관전화번호\n\nEXAMPLE USAGE:\n```bash\ncurl -X GET \\\n  "https://apis.data.go.kr/6450000/childfoodcard/getChildWelfareCardList?serviceKey={YOUR_API_KEY}&pageNo=1&numOfRows=10" \\\n  -H "Authorization: Infuser {YOUR_API_KEY}"\n```\n\n```python\nimport requests\n\nurl = "https://apis.data.go.kr/6450000/childfoodcard/getChildWelfareCardList"\nheaders = {\n    "Authorization": "Infuser {YOUR_API_KEY}"\n}\nparams = {\n    "serviceKey": "{YOUR_API_KEY}",\n    "pageNo": 1,\n    "numOfRows": 10\n}\nresponse = requests.get(url, headers=headers, params=params)\ndata = response.json()\nprint(data)\n```\n```',
            "llm_model": "gpt-4o mini",
            "token_count": 362,
        }
        markdown 필드의 데이터가 표준 문서로 다음과 같은 정보를 담고 있습니다.
        데이터의 형식, 요청 방법, 응답 형식, 예시 사용법 등을 포함하고 있습니다.
        이 데이터를 통해 사용자가 원하는 데이터를 찾을 수 있습니다.
        사용자가 원하는 데이터를 찾기 위해서는 다음과 같은 절차를 따라야 합니다.
        1. 사용자가 원하는 데이터의 키워드를 입력합니다.
        2. 입력된 키워드를 통해 search_api 툴을 통해 데이터를 검색합니다.
        3. 검색된 데이터 중 하나를 선택합니다.
        4. 선택된 데이터를 통해 get_std_docs 툴을 통해 표준 문서를 요청합니다.
        """
