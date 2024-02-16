from fastapi import HTTPException


class SAMLAuthError(HTTPException):
    def __init__(self, code: int, detail: any) -> None:
        self.status_code = code
        self.detail = detail
