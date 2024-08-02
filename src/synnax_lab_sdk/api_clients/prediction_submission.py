import sys
from typing import Dict, List, TypedDict, cast

from synnax_lab_sdk.http_client.bearer_token import HttpBearerTokenClient

if sys.version_info >= (3, 11):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired


class Submission(TypedDict):
    id: str
    datasetDate: str
    originalFilename: str
    confidenceScore: NotRequired[float]
    statusReason: NotRequired[str]
    status: str
    uploadedAt: NotRequired[str]
    ownerId: str


class CreateSubmissionRequest(TypedDict):
    datasetDate: str
    filename: str


class CreateSubmissionResponse(Submission):
    uploadUrl: str


class ListSubmissionsResponse(TypedDict):
    items: List[Submission]


class PublicCompanyPredictionSubmissionClient:
    def __init__(self, http_client: HttpBearerTokenClient):
        self.http_client = http_client

    def create_submission(
        self, request: CreateSubmissionRequest
    ) -> CreateSubmissionResponse:
        response = self.http_client.post("/submissions/create", cast(Dict, request))
        return cast(CreateSubmissionResponse, response)

    def list_submissions(self) -> ListSubmissionsResponse:
        response = self.http_client.post("/submissions/list", {})
        return cast(ListSubmissionsResponse, response)
