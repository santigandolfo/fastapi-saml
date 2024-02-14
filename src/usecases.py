from urllib.parse import urlencode

from entities import User
from error_codes import NO_SAML_RESPONSE_FROM_IDP
from errors import SAMLAuthError
from saml2 import BINDING_HTTP_POST
from saml2.client import Saml2Client
from utils import get_custom_jwt


class SamlUsecases:
    def __init__(self, saml_client: Saml2Client, frontend_url: str):
        self.saml_client = saml_client
        self.frontend_url = frontend_url

    def signin(self) -> str:
        _, info = self.saml_client.prepare_for_authenticate()
        redirect_url = dict(info["headers"]).get("Location", "")
        return redirect_url

    def _get_authn_response(self, saml_response: str):
        try:
            return self.saml_client.parse_authn_request_response(
                saml_response, BINDING_HTTP_POST
            )
        except Exception:
            return None

    def acs(self, saml_response: str) -> str:
        authn_response = self._get_authn_response(saml_response=saml_response)
        if not authn_response:
            raise SAMLAuthError(
                code=500,
                detail={
                    "error_code": NO_SAML_RESPONSE_FROM_IDP,
                    "reason": "There was an error creating the SAML client.",
                },
            )
        identity = authn_response.get_identity()
        user = User(**identity)
        jwt_params = get_custom_jwt(user=user)
        return f"{self.frontend_url}/?{urlencode(jwt_params)}"
