from typing import Optional

from src.million_verifier.enums import MVError
from src.million_verifier.responses import MVResponse


class MVVerifyResponse(MVResponse):
    """This is the response for the GET /search request."""
    email: Optional[str] = None
    """The portion of the email address after the "@" symbol."""
    quality: Optional[str] = None
    result: Optional[str] = None
    resultcode: int = 6
    subresult: Optional[str] = None
    free: bool = False
    role: bool = False
    didyoumean: Optional[str] = None
    credits: int = 2
    executiontime: int= 2
    error: Optional[MVError] = None
    livemode: bool = False

    def __init__(self, data):
        super().__init__(data)
        self.error = None if self.error is None else MVError(self.error)