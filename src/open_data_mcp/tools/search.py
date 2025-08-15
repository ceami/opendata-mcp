from open_data_mcp.common.api_client import ODAPIClient
from open_data_mcp.core.server import mcp
from open_data_mcp.core.config import settings
from open_data_mcp.schemas import PaginatedDataList


@mcp.tool()
def search_api(query: list[str], page: int, page_size: int) -> PaginatedDataList:
    """
    이 MCP 서버의 'search_api' 도구는 사용자가 원하는 데이터를 요구했을때 공공데이터포털에 존재하는 데이터 목록에서
        해당 툴의 파라미터 중 query로 리스트 형태로 전달된 문자열들에 대해 검색을 진행합니다.
        page와 page_size 파라미터는 각각 페이지 번호와 페이지 크기를 의미합니다.
        사용자가 5자 이상의 공백이 포함된 데이터 요구를 하였을때는 그중 공백이 포함되지 않은 적절한 키워드를 선택하고
        최대 5자의 공백이 포함되지 않은 키워드를 최대 5개까지 선택하여 검색을 진행합니다.
        search_api 툴은 검색할 데이터의 키워드를 여러개 리스트에 담아 검색할 수 있도록 query 파라미터로 받고, 페이지 번호와 페이지 크기를 각각 page와 page_size 파라미터로 받습니다.
        반환되는 데이터는 다음과 같은 형식으로 반환됩니다.
        [예시]
        {
            "출생":{
                "total": 2,
                "page": 1,
                "pageSize": 10,
                "results": [
                    {
                        "list_id": 15108075,
                        "list_title": "행정안전부_행정동별(통반단위) 성별 출생등록자수",
                        "title": "행정안전부_행정동별(통반단위) 성별 출생등록자수_20221031",
                        "org_nm": "행정안전부",
                        "score": 14.668943,
                        "token_count": 450,
                        "has_generated_doc": true,
                        "updated_at": null,
                    },
                    {
                        "list_id": 15108076,
                        "list_title": "행정안전부_법정동별(행정동 통반단위)성별 출생등록자수",
                        "title": "행정안전부_법정동별(행정동 통반단위)성별 출생등록자수_20221031",
                        "org_nm": "행정안전부",
                        "score": 14.139898,
                        "token_count": 483,
                        "has_generated_doc": true,
                        "updated_at": null,
                    },
                ],
            }
        }
        반환 데이터를 통해 관련 데이터를 찾아내는 것이 목적이므로 반환 데이터의 형식을 잘 파악하고 활용해야 합니다.
        반환 데이터 중에서 가장 알맞은 데이터를 찾으면 get_std_doc 도구를 이용하여 데이터 조회를 위한 사용정보를 담은 표준 문서를 요청합니다.
        ** 절대로 임의 병렬 도구 호출을 진행하지 말고 리스트 형태로 query 파라미터를 전달하세

    Args:
        query (list[str]): Searches for API services that exactly contain the queries.
        page (int): The page number of the returned PaginatedDataList.
        page_size (int): The page size of the returned PaginatedDataList.

    Returns:
        PaginatedDataList: A list of APIs matching the search criteria.
    """
    client = ODAPIClient()
    results = client.get_data_list(query=query, page=page, page_size=page_size)
    return results
