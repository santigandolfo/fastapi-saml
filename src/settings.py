from datetime import timedelta

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from saml2 import BINDING_HTTP_POST
from saml2 import BINDING_HTTP_REDIRECT


class Saml2Auth(BaseModel):
    frontend_url: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    jwt_secret: str
    jwt_algorithm: str
    access_token_lifetime: timedelta
    refresh_token_lifetime: timedelta
    remote_metadata: str
    allow_unknown_attributes: bool
    debug: bool
    entity_id: str
    want_assertions_signed: bool
    want_response_signed: bool
    allow_unsolicited: bool
    frontend_url: str

    def get_saml_config(self) -> dict:
        return {
            "metadata": {"remote": [{"url": self.remote_metadata}]},
            "allow_unknown_attributes": self.allow_unknown_attributes,
            "debug": self.debug,
            "entityid": self.entity_id,
            "service": {
                "sp": {
                    "endpoints": {
                        "assertion_consumer_service": [
                            (self.entity_id, BINDING_HTTP_REDIRECT),
                            (self.entity_id, BINDING_HTTP_POST),
                        ],
                    },
                    "allow_unsolicited": self.allow_unsolicited,
                    "want_assertions_signed,": self.want_assertions_signed,
                    "want_response_signed": self.want_response_signed,
                },
            },
        }


settings = Settings()
