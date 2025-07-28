import httpx
from open_data_mcp.schemas import PaginatedAPIList


class ODCloudAPI:
    """A client for the Public Data Utilization Support Center's list retrieval service."""

    def __init__(self, api_key: str):
        """Initializes the ODCloudAPI client.

        Args:
            api_key (str): The API key for the Public Data Utilization Support Center.
        """
        self.base_url = "https://api.odcloud.kr/api"
        self.headers = {"Authorization": f"Infuser {api_key}"}
        self.client = httpx.Client(headers=self.headers)

    def get_api_list(self, query: str, page: int, page_size: int) -> PaginatedAPIList:
        """Sends a GET request to search for API services using the Public Data Utilization Support Center's list retrieval service.

        Args:
            query (str): The search keyword.
            page (int): The page number.
            page_size (int): The number of items per page.

        Returns:
            PaginatedAPIList: A list of APIs matching the search criteria.
        """
        return PaginatedAPIList(
            **self.client.get(
                f"{self.base_url}/15077093/v1/open-data-list",
                params={"page": page, "perPage": page_size, "cond[title::LIKE]": query},
            ).json()
        )


class API:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {"Authorization": f"Infuser {api_key}"}
        self.client = httpx.Client(headers=self.headers)
