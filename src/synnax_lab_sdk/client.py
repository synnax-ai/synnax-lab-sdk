import os
from typing import List

from synnax_lab_sdk.api_clients.dataset import PublicCompanyDatasetClient
from synnax_lab_sdk.api_clients.prediction_submission import (
    PublicCompanyPredictionSubmissionClient,
    Submission,
)
from synnax_lab_sdk.constants import (
    PUBLIC_COMPANY_DATASET_URL,
    PUBLIC_COMPANY_PREDICTION_SUBMISSION_URL,
)
from synnax_lab_sdk.files_client import DatasetFilePaths, FilesClient
from synnax_lab_sdk.helpers.timedelta import iso_to_timedelta, pretty_timedelta
from synnax_lab_sdk.http_client.bearer_token import HttpBearerTokenClient
from synnax_lab_sdk.http_client.request import RequestHttpClient


class DatasetFiles(DatasetFilePaths):
    dataset_date: str


class SynnaxLabClient:
    def __init__(
        self,
        api_key: str,
        working_data_folder_path: str = "synnax-data",
        dataset_api_url: str = PUBLIC_COMPANY_DATASET_URL,
        prediction_submission_api_url: str = PUBLIC_COMPANY_PREDICTION_SUBMISSION_URL,
    ):
        self.working_data_folder_path = working_data_folder_path
        self.dataset_client = PublicCompanyDatasetClient(
            HttpBearerTokenClient(RequestHttpClient(dataset_api_url), lambda: api_key)
        )
        self.prediction_submission_client = PublicCompanyPredictionSubmissionClient(
            HttpBearerTokenClient(
                RequestHttpClient(prediction_submission_api_url),
                lambda: api_key,
            )
        )
        self.files_client = FilesClient(self.working_data_folder_path)

    def get_datasets(self) -> DatasetFiles:
        download_info = self.dataset_client.download_datasets()
        print(f'Downloading datasets for {download_info["date"]}...')
        files = self.files_client.download_and_extract_datasets(
            download_info["fileUrl"]
        )
        duration_remaining = iso_to_timedelta(
            download_info["durationLeftForSubmissions"]
        )
        print(
            f"You have {pretty_timedelta(duration_remaining)} remaining to train and submit your predictions"
        )
        return {**files, "dataset_date": download_info["date"]}

    def submit_predictions(self, dataset_date: str, submission_file_path: str) -> None:
        upload_info = self.prediction_submission_client.create_submission(
            {
                "datasetDate": dataset_date,
                "filename": os.path.basename(submission_file_path),
            }
        )
        print(
            f'Uploading submission {upload_info["id"]} for {upload_info["datasetDate"]}...'
        )
        self.files_client.upload_submission(
            submission_file_path, upload_info["uploadUrl"]
        )
        print(f'Uploaded submission {upload_info["id"]}')

    def get_past_submissions(self) -> List[Submission]:
        past_submissions = self.prediction_submission_client.list_submissions()
        print(
            "{:<38} {:<12} {:<20} {:<20}".format(
                "ID",
                "Date",
                "Status",
                "Score",
            )
        )
        for submission in past_submissions["items"]:
            print(
                "{:<38} {:<12} {:<20} {:<20}".format(
                    submission.get("id"),
                    submission.get("datasetDate"),
                    submission.get("status"),
                    submission.get("confidenceScore", "N/A"),
                )
            )

        return past_submissions["items"]
