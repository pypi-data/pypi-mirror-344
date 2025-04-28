from src.mine_lead.enums import MLSearchStatus
from src.mine_lead.responses import MLSearchEmailResponse, MLResponse


class MLSearchResponse(MLResponse):
    """This is the response for the GET /search request."""
    domain: str = None
    """The portion of the email address after the "@" symbol."""

    status: MLSearchStatus = None

    pattern: str = None

    emails: list[MLSearchEmailResponse] = []

    def __init__(self, data):
        super().__init__(data)
        if self.status:
            if self.status == "not found":
                self.status = MLSearchStatus.not_found
            else:
                self.status = MLSearchStatus(self.status)
        if 'emails' in data:
            self.emails = [MLSearchEmailResponse(data) for data in data.get('emails')]