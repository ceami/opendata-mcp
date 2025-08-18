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
    ODP_SERVICE_KEY: str | None = None

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
    cli_args = parser.parse_args()
    if cli_args.transport is not None:
        config_data["transport"] = cli_args.transport
    return Settings(**config_data)


settings = load_settings()
