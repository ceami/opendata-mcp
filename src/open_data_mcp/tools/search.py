from open_data_mcp.common.api_client import ODCloudAPI
from open_data_mcp.core.server import mcp
from open_data_mcp.core.config import settings


@mcp.tool()
def search_api(query: str):
    """
    공공데이터 포털에서 제공되는 api 서비스 중에서 입력되는 query와 연관된 서비스를 검색하여 리스트로 return 합니다.
    """
    client = ODCloudAPI(api_key=settings.data_portal_api_key)
    return client.get_api_list(query=query)
