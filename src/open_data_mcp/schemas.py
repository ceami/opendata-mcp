from pydantic import BaseModel, ConfigDict, AliasGenerator, field_validator, Field
from pydantic.alias_generators import to_camel
from typing import Literal
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
    current_count: int
    match_count: int
    page: int
    per_page: int
    total_count: int


class APIInfo(BaseModel):
    api_type: str
    category_nm: str
    core_data_nm: str | None
    created_at: datetime | None = Field(default=None)
    data_format: str
    dept_nm: str | None
    desc: str
    end_point_url: str
    guide_url: str | None
    id: str
    is_charged: str
    is_confirmed_for_dev: Literal["Y", "N"]
    is_confirmed_for_dev_nm: str
    is_confirmed_for_prod: Literal["Y", "N"]
    is_confirmed_for_prod_nm: str
    is_copyrighted: Literal["Y", "N"]
    is_core_data: Literal["Y", "N"]
    is_deleted: Literal["Y", "N"]
    is_list_deleted: Literal["Y", "N"]
    is_std_data: Literal["Y", "N"]
    is_third_party_copyrighted: str
    keywords: list[str]
    link_url: str
    list_id: int
    list_title: str
    list_type: str
    meta_url: str
    new_category_cd: str
    new_category_nm: str
    operation_nm: str | None = Field(default=None)
    operation_seq: int | None = Field(default=None)
    operation_url: str | None = Field(default=None)
    org_cd: str
    org_nm: str
    ownership_grounds: str | None = Field(default=None)
    register_status: str
    request_cnt: int
    request_param_nm: list[str] | None = Field(default=None)
    request_param_nm_en: list[str] | None = Field(default=None)
    response_param_nm: list[str] | None = Field(default=None)
    response_param_nm_en: list[str] | None = Field(default=None)
    share_scope_cd: str
    share_scope_nm: str
    share_scope_reason: str
    soap_url: str
    title: str
    title_en: str
    updated_at: datetime | None = Field(default=None)
    upper_category_cd: str
    use_prmisn_ennc: str

    @field_validator(
        "keywords",
        "request_param_nm",
        "request_param_nm_en",
        "response_param_nm",
        "response_param_nm_en",
        mode="before",
    )
    @staticmethod
    def str_list_validator(v: str):
        if v:
            v = v.replace('"', "")
            str_list = v.split(",")
            v = [str.strip(item) for item in str_list]
        return v

    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def datetime_validator(cls, v: str):
        if v:
            return datetime.strptime(v, "%Y-%m-%d")
        return None


class PaginatedAPIList(PaginatedResponse):
    data: list[APIInfo]
