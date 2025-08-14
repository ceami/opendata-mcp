import httpx
from open_data_mcp.schemas import PaginatedDataList, StdDocsInfo
from open_data_mcp.core.config import settings


class ODAPIClient:
    def __init__(self):
        self.base_url = settings.api_url
        self.client = httpx.Client()

    def get_data_list(self, q: str, page: int, page_size: int) -> PaginatedDataList:
        """Sends a GET request to search for API services using the open data service.

        Args:
            query (str): The search keyword.
            page (int): The page number.
            page_size (int): The number of items per page.

        Returns:
            PaginatedDataList: A list of data matching the search criteria.
        """
        return PaginatedDataList(
            **self.client.get(
                f"{self.base_url}/api/v1/search/title",
                params={"q": q, "page": page, "page_size": page_size},
            ).json()
        )

    def get_std_docs(self, list_id: int) -> StdDocsInfo:
        """Returns a standard document for the given list ID.

        Args:
            list_id (int): The list ID of the data to get the standard document for.
        """
        return StdDocsInfo(
            **self.client.get(
                f"{self.base_url}/api/v1/document/std-docs/{list_id}"
            ).json()
        )
