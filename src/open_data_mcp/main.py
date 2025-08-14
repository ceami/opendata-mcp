from open_data_mcp.core.server import mcp
from open_data_mcp.core.config import settings
import open_data_mcp.tools.search  # noqa: F401
import open_data_mcp.prompts.search  # noqa: F401


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
            path="/",
        )


if __name__ == "__main__":
    main()
