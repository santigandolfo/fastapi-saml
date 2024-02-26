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
    entityid: str
    want_response_signed: bool
    frontend_url: str

    def get_saml_config(self) -> dict:
        return {
            "metadata": {"remote": [{"url": self.remote_metadata}]},
            "allow_unknown_attributes": True,
            "debug": self.debug,
            "entityid": self.entityid,
            "service": {
                "sp": {
                    "endpoints": {
                        "assertion_consumer_service": [
                            (self.entityid, BINDING_HTTP_REDIRECT),
                            (self.entityid, BINDING_HTTP_POST),
                        ],
                    },
                    "allow_unsolicited": True,
                    "want_response_signed": self.want_response_signed,
                },
            },
        }


settings = Settings()
