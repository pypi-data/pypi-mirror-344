import requests

from src.mine_lead.exceptions import MLClientException, MLApiException
from src.mine_lead.responses import MLSearchResponse


class MineLead:
    BASE_URL = "https://api.minelead.io/v1"

    def __init__(self, api_key: str):
        if not api_key.strip():
            raise MLClientException("Empty parameter: api_key")
        self._api_key = api_key

    def _get(self, url, response_class, params=None):
        if not params:
            params = {}
        params["key"] = self._api_key
        response = requests.get(url, params=params)

        try:
            json_response = response.json()
        except ValueError as e:
            raise MLApiException from e

        error = json_response["status"]
        if error is "error":
            raise MLApiException(json_response['message'])
        else:
            return response_class(json_response)

    def _post(self, url, response_class, data=None, json=None, files=None):
        response = requests.post(url, data=data, json=json, files=files)

        try:
            json_response = response.json()
        except ValueError as e:
            raise MLApiException('Request not processed succesfully. Status code %s' % response.status_code)
        if json_response:
            return response_class(json_response)
        return None

    def search(self, domain: str, name: str = None, max_emails: int = 4):
        """Search for leads.

        Parameters
        ----------
        domain: str
            The email address you want to validate
        name: ``str`` or ``None``
            If no domain is provided and name is given, search will be based on name
        max_emails: ``int``
            Display a maximum of 4 emails for a domain (optional)


        Raises
        ------
        MineleadApiException

        Returns
        -------
        response: MLSearchResponse
            Returns a MLSearchResponse object if the request was successful

        """

        return self._get(
            f"{self.BASE_URL}/search",
            MLSearchResponse,
            params={
                "domain": domain,
                "name": name,
                'max-emails': max_emails
            },
        )