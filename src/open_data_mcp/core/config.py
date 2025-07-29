from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from argparse import ArgumentParser


class Settings(BaseSettings):
    log_level: str = "INFO"
    data_portal_api_key: str | None
    transport: str = "stdio"
    host: str = "127.0.0.1"
    port: int = 3000
    model_config = ConfigDict(
        extra="ignore",
    )


def load_settings():
    """Loads the settings from the command line arguments.

    Returns:
        Settings: The settings object.
    """
    config_data = {}
    parser = ArgumentParser(description="MCP Server Command Line Settings")
    parser.add_argument(
        "--data-portal-api-key",
        type=str,
        help="Public Data Portal API Key",
        required=True,
    )
    parser.add_argument(
        "--transport",
        type=str,
        help="stdio or http or sse.",
        required=False,
    )
    parser.add_argument(
        "--host",
        type=str,
        help="Host addr for http/sse transport.",
        required=False,
    )
    parser.add_argument(
        "--port",
        type=int,
        help="Port for http/sse transport.",
        required=False,
    )
    parser.add_argument(
        "--path",
        type=str,
        help="Path for http/sse transport.",
        required=False,
    )

    cli_args = parser.parse_args()
    if cli_args.data_portal_api_key is not None:
        config_data["data_portal_api_key"] = cli_args.data_portal_api_key
    if cli_args.transport is not None:
        config_data["transport"] = cli_args.transport
    if cli_args.host is not None:
        config_data["host"] = cli_args.host
    if cli_args.port is not None:
        config_data["port"] = cli_args.port
    return Settings(**config_data)


settings = load_settings()
