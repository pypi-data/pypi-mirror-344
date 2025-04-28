from typing import Optional

from src.million_verifier.responses import MVFileResponse


class MVGetFileResponse(MVFileResponse):
    """This is the response for the GET /download request."""

    success: bool = True

    file_name: Optional[str] = None