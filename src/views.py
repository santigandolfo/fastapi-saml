from fastapi import APIRouter
from fastapi import Form
from fastapi.responses import RedirectResponse
from saml2.client import Saml2Client
from saml2.config import Config as Saml2Config

from src.settings import settings
from src.usecases import SamlUsecases

router = APIRouter(tags=["saml"])

config = Saml2Config()
config.load(settings.get_saml_config())
saml_client = Saml2Client(config=config)
saml_usecases = SamlUsecases(saml_client, settings.frontend_url)


@router.get("/accounts/login/", response_class=RedirectResponse, status_code=302)
async def signin() -> str:
    return saml_usecases.signin()


@router.post("/saml2_auth/acs/", response_class=RedirectResponse, status_code=302)
async def acs(saml_response: str = Form(alias="SAMLResponse")) -> str:
    return saml_usecases.acs(saml_response=saml_response)
