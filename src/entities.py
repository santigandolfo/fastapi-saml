from typing import get_origin

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo


class ParamsBaseModel(BaseModel):
    @field_validator("*", mode="before")
    @classmethod
    def validate_value(cls, value: any, info: ValidationInfo) -> any:
        value_type = cls.model_fields[info.field_name].annotation
        if value_type is list or get_origin(value_type) is list:
            return value
        return value[-1]


class User(ParamsBaseModel):
    model_config = ConfigDict(populate_by_name=True)

    email: str = Field(validation_alias="user.email")
    first_name: str = Field(validation_alias="user.first_name")
    last_name: str = Field(validation_alias="user.last_name")
    username: str = Field(validation_alias="user.username")
    groups: list[str] = Field(validation_alias="Groups")
