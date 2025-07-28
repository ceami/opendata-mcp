from open_data_mcp.core.server import mcp


@mcp.prompt()
def introduce_project() -> str:
    return "이 MCP 서버는 공공데이터포털의 공공데이터활용지원센터_목록조회서비스를 활용하여 주제에 맞는 공공데이터 검색 및 분석 기능을 제공합니다."


@mcp.prompt()
def search_api_usage_guide():
    """
    search_api 툴의 사용법을 반환합니다.
    """
    return """
        이 MCP 서버의 'search_api' 도구는 사용자가 원하는 데이터를 요구했을때 공공데이터포털에 존재하는 데이터 목록에서
        해당 툴의 파라미터 중 query로 전달된 문자열이 포함된 제목을 가지고 있는 서비스를 최대 100개 반환합니다.
        사용자가 5자 이상의 공백이 포함된 데이터 요구를 하였을때는 그중 공백이 포함되지 않은 적절한 키워드를 선택하고
        선택한 공백이 미포함된 키워드를 search_api툴을 호출할 때 사용해야 연관 데이터를 원활하게 얻을 수 있습니다.
        search_api 툴은 검색할 데이터의 키워드를 query 파라미터로 받고, 페이지 번호와 페이지 크기를 각각 page와 page_size 파라미터로 받습니다.
        [반환되는 데이터 예시] 
        {"currentCount": 1, "data": [{
            "api_type": "REST",
            "category_nm": "교통및물류 > 철도",
            "core_data_nm": null,
            "created_at": "2014-08-25T00:00:00",
            "data_format": "XML",
            "dept_nm": "기획예산실",
            "desc": "부산 도시철도 해당역에서 제공되고 있는 장애인 편의시설들을 조회하는 서비스",
            "end_point_url": "http://data.humetro.busan.kr/voc/api/open_api_convenience.tnn",
            "guide_url": "",
            "id": "uddi:907f592e-5a0c-41e4-8b7d-89cef6f564b3",
            "is_charged": "무료",
            "is_confirmed_for_dev": "Y",
            "is_confirmed_for_dev_nm": "자동승인",
            "is_confirmed_for_prod": "Y",
            "is_confirmed_for_prod_nm": "자동승인",
            "is_copyrighted": "N",
            "is_core_data": "N",
            "is_deleted": "N",
            "is_list_deleted": "N",
            "is_std_data": "N",
            "is_third_party_copyrighted": "없음",
            "keywords": ["부산지하철", "장애인편의시설", "이동약자편의시설"],
            "link_url": " ",
            "list_id": 15001020,
            "list_title": "부산교통공사_부산도시철도 장애인 편의시설 정보",
            "list_type": "PR0027",
            "meta_url": "https://www.data.go.kr/catalog/15001020/openapi.json",
            "new_category_cd": "OC0011",
            "new_category_nm": "교통물류",
            "operation_nm": "부산 도시철도 장애인 편의시설 정보",
            "operation_seq": 4575,
            "operation_url": null,
            "org_cd": "B551542",
            "org_nm": "부산교통공사",
            "ownership_grounds": null,
            "register_status": "등록승인",
            "request_cnt": 141,
            "request_param_nm": [
                "xml",
                "json",
                "xls",
                "역외부코드(ex.신평:101",
                "안평:414)",
            ],
            "request_param_nm_en": ["act", "scode"],
            "response_param_nm": [
                "",
                "해당 역사 보유 휠체어 리프트(내부) 개수",
                "해당 역사 보유 휠체어 리프트(외부) 개수",
                "해당 역사 보유 엘리베이터(내부) 개수",
                "해당 역사 보유 엘리베이터(외부) 개수",
                "해당 역사 보유 에스컬레이터 개수",
                "해당 역사 보유 시각장애인유도로 개수",
                "해당 역사 보유 외부경사로 개수",
                "해당 역사 보유 승차보조대 개수",
                "해당 역사 보유 장애인화장실 개수",
                "공용",
                "분리",
            ],
            "response_param_nm_en": [
                "sname",
                "wl_i",
                "wl_o",
                "el_i",
                "el_o",
                "es",
                "blindroad",
                "ourbridge",
                "helptake",
                "toilet",
                "toilet_gubun",
            ],
            "share_scope_cd": "PBDE07",
            "share_scope_nm": "행정/공공/민간",
            "share_scope_reason": "",
            "soap_url": " ",
            "title": "부산 도시철도 장애인 편의시설 정보",
            "title_en": "Busan Metro Meeting Facility Information",
            "updated_at": "2024-07-28T00:00:00",
            "upper_category_cd": "NB000120061201100059544",
            "use_prmisn_ennc": "없음",
        }], "matchCount": 1, "page": 1, "perPage": 1, "totalCount": 1}
        "data" 키에 포함된 데이터에서 사용자가 요구한 데이터에 가장 일치하는 서비스를 제공하면 됨.
        데이터 하나 당 key를 30개 이상 가지고 있기 때문에 사용자에게 데이터를 제공할때에는 표로 정리해서 한눈에 알아볼 수 있게 정리하고
        is_deleted 와 is_list_deleted의 값이 Y 일 경우에는 데이터 선택 우선순위에서 후순위로 판단
        제공하는 데이터에 꼭 포함되어야 하는 데이터의 키 값은 아래와 같음
        api_type(api 타입), category_nm(데이터 분류), core_data_nm(핵심 데이터 이름), data_format(데이터 형식/"json 또는 XML"), dept_nm(데이터 제공 기관명), desc(데이터 설명), end_point_url(서비스 엔드포인트 URL), guide_url(서비스 가이드 URL), is_charged(요금 정보), is_confirmed_for_dev_nm(개발 계정 승인), is_confirmed_for_prod_nm(운영 계정 승인), is_copyrighted(저작권 여부),
        is_core_data(핵심 데이터 여부), is_deleted, is_list_deleted, is_std_data(표준 데이터 여부), is_third_party_copyrighted(제 3자 저작권 여부), keywords(키워드 리스트), link_url(링크), list_title(목록 제목), meta_url(메타데이터 URL), new_category_nm(데이터 분류2), operation_nm(오퍼레이션 이름), operation_url(오퍼레이션 URL), org_nm(기관 명), register_status(데이터 등록상태),
        request_cnt(요청 횟수), request_param_nm(요청 파라미터 이름), request_param_nm_en(요청 파라미터 영문 이름), response_param_nm(응답 파라미터 이름), response_param_nm_en(응답 파라미터 영문 이름), sname(영문 키워드), share_scope_nm(공유 범위명), title(제목) 
        """
