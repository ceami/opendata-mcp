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
    config_data = {}
    parser = ArgumentParser(description="MCP 서버 Command Line 설정")
    parser.add_argument(
        "--data-portal-api-key", type=str, help="공공데이터포털 API 키", required=True
    )
    cli_args = parser.parse_args()
    if cli_args.data_portal_api_key is not None:
        config_data["data_portal_api_key"] = cli_args.data_portal_api_key
    return Settings(**config_data)


settings = load_settings()
