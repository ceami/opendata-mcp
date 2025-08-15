import httpx
from open_data_mcp.schemas import PaginatedDataList, StdDocsInfo
from open_data_mcp.core.config import settings


class ODAPIClient:
    def __init__(self):
        self.base_url = f"https://{settings.api_host}"
        self.api_version_prefix = "/api/v1"
        self.client = httpx.Client()

    def get_data_list(
        self, query: list[str], page: int, page_size: int
    ) -> PaginatedDataList:
        """Sends a GET request to search for API services using the open data service.

        Args:
            query (list[str]): The search keyword .
            page (int): The page number.
            page_size (int): The number of items per page.

        Returns:
            PaginatedDataList: A list of data matching the search criteria.
        """
        return PaginatedDataList(
            **self.client.get(
                f"{self.base_url}{self.api_version_prefix}/search/title",
                params={"query": query, "page": page, "page_size": page_size},
            ).json()
        )

    def get_std_docs(self, list_id: list[int]) -> list[StdDocsInfo]:
        """Returns a standard document for the given list ID.

        Args:
            list_id (list[int]): The list ID of the data to get the standard document for.
        """
        results = self.client.get(
            f"{self.base_url}{self.api_version_prefix}/document/std-docs",
            params={"list_ids": list_id, "page": 1, "page_size": len(list_id)},
        ).json()
        return [StdDocsInfo(**result) for result in results]
