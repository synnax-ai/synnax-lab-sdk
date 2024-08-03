from typing import TypedDict, cast

from synnax_lab_sdk.http_client.bearer_token import HttpBearerTokenClient


class DownloadDatasetsResponse(TypedDict):
    date: str
    fileUrl: str
    submissionDeadline: str


class PublicCompanyDatasetClient:
    def __init__(self, http_client: HttpBearerTokenClient):
        self.http_client = http_client

    def download_datasets(self) -> DownloadDatasetsResponse:
        response = self.http_client.post("/datasets/download", {})
        return cast(DownloadDatasetsResponse, response)
