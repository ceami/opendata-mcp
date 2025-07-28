from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from argparse import ArgumentParser


class Settings(BaseSettings):
    log_level: str = "INFO"
    data_portal_api_key: str | None
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
    cli_args = parser.parse_args()
    if cli_args.data_portal_api_key is not None:
        config_data["data_portal_api_key"] = cli_args.data_portal_api_key
    return Settings(**config_data)


settings = load_settings()
