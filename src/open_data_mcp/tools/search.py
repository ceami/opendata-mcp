from open_data_mcp.common.api_client import ODAPIClient
from open_data_mcp.core.server import mcp
from open_data_mcp.core.config import settings
from open_data_mcp.schemas import PaginatedDataList


@mcp.tool()
def search_api(
    query: list[str], page: int, page_size: int
) -> dict[str, PaginatedDataList]:
    """Returns a list of API services provided by the open data service that exactly match the input query.

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
