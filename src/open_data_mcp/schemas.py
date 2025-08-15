from pydantic import BaseModel, ConfigDict, AliasGenerator, Field
from pydantic.alias_generators import to_camel
from typing import Literal, Any
from datetime import datetime


class BaseModelWithConfig(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
            serialization_alias=to_camel,
        ),
        validate_by_name=True,
        from_attributes=True,
        extra="ignore",
    )


class PaginatedResponse(BaseModelWithConfig):
    total: int
    page: int
    page_size: int


class DataInfo(BaseModelWithConfig):
    list_id: int
    list_title: str
    org_nm: str
    token_count: int
    has_generated_doc: bool
    updated_at: datetime | None
    data_type: str
    score: float


class StdDocsInfo(BaseModelWithConfig):
    id: str
    list_id: int
    detail_url: str
    markdown: str
    llm_model: str
    token_count: int


class PaginatedDataList(PaginatedResponse):
    results: list[DataInfo]


# New schemas for generic API calls
class BaseInfo(BaseModelWithConfig):
    host: str
    base_path: str


class Param(BaseModelWithConfig):
    name: str
    description: str
    type: str
    required: bool
    value: Any | None = None


class EndpointInfo(BaseModelWithConfig):
    path: str
    method: str
    params: list[Param] = []
    headers: dict[str, str] | None = None
    body: dict[str, Any] | None = None


class RequestData(BaseModelWithConfig):
    base_info: BaseInfo
    endpoint_info: EndpointInfo
    request_parameters: dict[str, Any]
