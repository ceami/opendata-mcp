from open_data_mcp.common.api_client import ODAPIClient
from open_data_mcp.core.server import mcp
from open_data_mcp.schemas import StdDocsInfo


@mcp.tool()
def get_std_docs(list_id: int) -> StdDocsInfo:
    """Returns a standard document for the given list ID.

    Args:
        list_id (int): The list ID of the data to get the standard document for.

    Returns:
        StdDocsInfo: A standard document for the given list ID.
    """
    client = ODAPIClient()
    return client.get_std_docs(list_id)
