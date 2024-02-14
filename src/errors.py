from fastapi import HTTPException


class SAMLAuthError(HTTPException):
    def __init__(self, code, detail):
        self.status_code = code
        self.detail = detail
