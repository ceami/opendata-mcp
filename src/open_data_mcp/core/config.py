from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from argparse import ArgumentParser


class Settings(BaseSettings):
    log_level: str = "INFO"
    transport: str = "stdio"
    host: str = "127.0.0.1"
    port: int = 3000
    path: str = "/"
    api_url: str
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
    parser.add_argument(
        "--api-url",
        type=str,
        help="API URL for the open data service.",
        required=True,
    )

    cli_args = parser.parse_args()
    if cli_args.transport is not None:
        config_data["transport"] = cli_args.transport
    if cli_args.host is not None:
        config_data["host"] = cli_args.host
    if cli_args.port is not None:
        config_data["port"] = cli_args.port
    if cli_args.path is not None:
        config_data["path"] = cli_args.path
    if cli_args.api_url is not None:
        config_data["api_url"] = cli_args.api_url
    return Settings(**config_data)


settings = load_settings()
