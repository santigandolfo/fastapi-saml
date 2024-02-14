from fastapi import FastAPI
from views import router

app = FastAPI(
    title="FastAPI SAML2",
    version="1.0",
    description="Example API to implement SAML2 authentication in FastAPI",
)

app.include_router(router)
