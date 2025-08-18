from pydantic_settings import (
    BaseSettings,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
)
from argparse import ArgumentParser


class Settings(BaseSettings):
    name: str
    version: str
    description: str
    log_level: str = "INFO"
    transport: str = "stdio"
    host: str = "127.0.0.1"
    port: int = 8000
    api_host: str = "mcp.dev.ezrnd.co.kr"
    service_key: str | None = None

    model_config = SettingsConfigDict(
        extra="ignore",
        pyproject_toml_table_header=("project",),
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            PyprojectTomlConfigSettingsSource(settings_cls),
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
        "--service-key",
        type=str,
        help="Service key for the data.go.kr.",
        required=False,
    )

    cli_args = parser.parse_args()
    if cli_args.transport is not None:
        config_data["transport"] = cli_args.transport
    if cli_args.host is not None:
        config_data["host"] = cli_args.host
    if cli_args.port is not None:
        config_data["port"] = cli_args.port
    if cli_args.service_key is not None:
        config_data["service_key"] = cli_args.service_key
    return Settings(**config_data)


settings = load_settings()
