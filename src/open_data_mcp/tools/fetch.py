import ssl
import requests
from open_data_mcp.core.server import mcp
from open_data_mcp.core.config import settings
from open_data_mcp.schemas import RequestData


@mcp.tool()
def call_openapi_endpoint(request_data: str) -> dict:
    """
    Provided OpenAPI metadata, sends an API request to a specific endpoint.
    It dynamically generates requests by identifying the API's base information, path, method,
    and required/optional parameters, then processes the response.

    Args:
        request_data (RequestData): An object containing all necessary information for the API call.

    Returns:
        dict: The JSON response from the API.
    """
    request_data_obj = RequestData.model_validate_json(request_data)
    # Properly construct the full URL: host + base_path + path
    endpoint_url = f"http://{request_data_obj.base_info.host}{request_data_obj.base_info.base_path}{request_data_obj.endpoint_info.path}"

    params = request_data_obj.request_parameters.copy()
    headers = request_data_obj.endpoint_info.headers or {}

    # --- Service Key Injection Logic ---
    # 1. Check for serviceKey in query parameters
    for p in request_data_obj.endpoint_info.params:
        if "servicekey" in p.name.lower():
            params[p.name] = settings.data_portal_api_key
            break

    # 2. Check for serviceKey in headers (e.g., Authorization)
    if headers:
        for key in list(headers.keys()):
            if "authorization" in key.lower():
                # Assuming the key format is 'Infuser {key}' as is common in the platform
                headers[key] = f"Infuser {settings.data_portal_api_key}"
                break
    # --- End of Injection Logic ---

    try:
        method = request_data_obj.endpoint_info.method.upper()

        # Set default headers
        default_headers = {}
        if headers:
            default_headers.update(headers)

        if method == "GET":
            response = requests.get(
                endpoint_url,
                params=params,
                headers=default_headers,
                timeout=30,
                verify=False,
            )
        elif method == "POST":
            response = requests.post(
                endpoint_url,
                json=request_data_obj.endpoint_info.body,
                headers=default_headers,
                timeout=30,
                verify=False,
            )
        else:
            return {"error": "Unsupported HTTP method"}

        response.raise_for_status()
        return response.text

    except requests.exceptions.HTTPError as e:
        return {
            "error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while requesting: {e}"}
