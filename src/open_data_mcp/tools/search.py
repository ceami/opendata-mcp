from open_data_mcp.common.api_client import ODCloudAPI
from open_data_mcp.core.server import mcp
from open_data_mcp.core.config import settings
from open_data_mcp.schemas import PaginatedAPIList


@mcp.tool()
def search_api(query: str, page: int, page_size: int) -> PaginatedAPIList:
    """Returns a list of API services provided by the public data portal that exactly match the input query.

    Args:
        query (str): Searches for API services that exactly contain the query.
        page (int): The page number of the returned PaginatedAPIList.
        page_size (int): The page size of the returned PaginatedAPIList.

    Returns:
        PaginatedAPIList: A list of APIs matching the search criteria.
    """
    client = ODCloudAPI(api_key=settings.data_portal_api_key)
    return client.get_api_list(query=query, page=page, page_size=page_size)
