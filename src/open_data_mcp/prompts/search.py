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
        [반환되는 데이터 예시] 
        {"currentCount": 0, "data": [], "matchCount": 0, "page": 1, "perPage": 100, "totalCount": 16392}
        "data" 키에 해당하는 value 에서 사용자가 요구한 데이터에 가장 일치하는 서비스를 제공하면 됨.
        """
