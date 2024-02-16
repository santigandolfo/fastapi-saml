from urllib.parse import urlencode

from saml2 import BINDING_HTTP_POST
from saml2.client import Saml2Client
from saml2.response import AuthnResponse

from src.entities import User
from src.error_codes import NO_AUTHN_RESPONSE_IN_SAML_RESPONSE
from src.error_codes import NO_USER_IDENTITY_IN_SAML_RESPONSE
from src.errors import SAMLAuthError
from src.utils import get_custom_jwt


class SamlUsecases:
    def __init__(self, saml_client: Saml2Client, frontend_url: str) -> None:
        self.saml_client = saml_client
        self.frontend_url = frontend_url

    def signin(self) -> str:
        _, info = self.saml_client.prepare_for_authenticate()
        return dict(info["headers"]).get("Location", "")

    def _parse_saml_response(self, saml_response: str) -> AuthnResponse:
        try:
            authn_response = self.saml_client.parse_authn_request_response(
                saml_response, BINDING_HTTP_POST
            )
            if not authn_response:
                raise ValueError("Invalid SAML Response")
            return authn_response
        except Exception as e:
            raise SAMLAuthError(
                code=500,
                detail={
                    "error_code": NO_AUTHN_RESPONSE_IN_SAML_RESPONSE,
                    "error_detail": str(e),
                },
            ) from e

    @staticmethod
    def _get_identity(authn_response: AuthnResponse) -> dict:
        try:
            identity = authn_response.get_identity()
            if not identity:
                raise ValueError("Identity not found in response")
            return identity
        except Exception as e:
            raise SAMLAuthError(
                code=500,
                detail={
                    "error_code": NO_USER_IDENTITY_IN_SAML_RESPONSE,
                    "error_detail": str(e),
                },
            ) from e

    def acs(self, saml_response: str) -> str:
        authn_response = self._parse_saml_response(saml_response)
        identity = self._get_identity(authn_response)
        user = User(**identity)
        jwt_params = get_custom_jwt(user=user)
        return f"{self.frontend_url}/?{urlencode(jwt_params)}"
