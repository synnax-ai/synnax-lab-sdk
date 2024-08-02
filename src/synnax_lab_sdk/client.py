from synnax_lab_sdk.api_clients.dataset import PublicCompanyDatasetClient
from synnax_lab_sdk.api_clients.prediction_submission import (
    PublicCompanyPredictionSubmissionClient,
)
from synnax_lab_sdk.constants import (
    PUBLIC_COMPANY_DATASET_URL,
    PUBLIC_COMPANY_PREDICTION_SUBMISSION_URL,
)
from synnax_lab_sdk.http_client.bearer_token import HttpBearerTokenClient
from synnax_lab_sdk.http_client.request import RequestHttpClient


class SynnaxLabClient:
    def __init__(self, api_key: str, working_folder_path: str):
        self.working_folder_path = working_folder_path
        self.dataset_client = PublicCompanyDatasetClient(
            HttpBearerTokenClient(
                RequestHttpClient(PUBLIC_COMPANY_DATASET_URL), lambda: api_key
            )
        )
        self.prediction_submission_client = PublicCompanyPredictionSubmissionClient(
            HttpBearerTokenClient(
                RequestHttpClient(PUBLIC_COMPANY_PREDICTION_SUBMISSION_URL),
                lambda: api_key,
            )
        )
