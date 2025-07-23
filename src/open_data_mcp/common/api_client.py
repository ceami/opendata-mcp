import httpx
from open_data_mcp.schemas import PaginatedAPIList


class ODCloudAPI:
    def __init__(self, api_key: str):
        self.base_url = "https://api.odcloud.kr/api"
        self.headers = {"Authorization": f"Infuser {api_key}"}
        self.client = httpx.Client(headers=self.headers)

    def get_api_list(self, query):
        return PaginatedAPIList(
            **self.client.get(
                f"{self.base_url}/15077093/v1/open-data-list",
                params={"page": 1, "perPage": 100, "cond[title::LIKE]": query},
            ).json()
        )
