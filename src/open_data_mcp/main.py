from open_data_mcp.core.server import mcp
from open_data_mcp.core.config import settings

from open_data_mcp.tools import search_api, call_openapi_endpoint, get_std_docs

tools = [search_api, call_openapi_endpoint, get_std_docs]


def main():
    if settings.transport == "stdio":
        mcp.run(
            transport=settings.transport,
        )
    else:
        mcp.run(
            transport=settings.transport,
            host=settings.host,
            port=settings.port,
        )


if __name__ == "__main__":
    main()
