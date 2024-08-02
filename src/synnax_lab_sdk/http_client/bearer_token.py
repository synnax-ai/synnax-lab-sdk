from typing import Callable, Dict

from synnax_lab_sdk.http_client.http_client import HttpClient


class HttpBearerTokenClient(HttpClient):
    def __init__(self, http_client: HttpClient, token_provider: Callable[[], str]):
        self.http_client = http_client
        self.token_provider = token_provider

    def post(self, endpoint: str, body: Dict, headers: Dict = {}) -> Dict:
        response = self.http_client.post(
            endpoint,
            body=body,
            headers={**headers, "Authorization": "Bearer " + self.token_provider()},
        )
        return response
