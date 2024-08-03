import os
from datetime import datetime, timezone
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
from synnax_lab_sdk.helpers.timedelta import pretty_timedelta
from synnax_lab_sdk.http_client.bearer_token import HttpBearerTokenClient
from synnax_lab_sdk.http_client.request import RequestHttpClient


class DatasetFiles(DatasetFilePaths):
    dataset_date: str


class SynnaxLabClient:
    def __init__(
        self,
        api_key: str,
        working_data_folder_path: str = "synnax-data",
        verbose: bool = True,
        dataset_api_url: str = PUBLIC_COMPANY_DATASET_URL,
        prediction_submission_api_url: str = PUBLIC_COMPANY_PREDICTION_SUBMISSION_URL,
    ):
        self.working_data_folder_path = working_data_folder_path
        self.verbose = verbose
        self.dataset_client = PublicCompanyDatasetClient(
            HttpBearerTokenClient(RequestHttpClient(dataset_api_url), lambda: api_key)
        )
        self.prediction_submission_client = PublicCompanyPredictionSubmissionClient(
            HttpBearerTokenClient(
                RequestHttpClient(prediction_submission_api_url),
                lambda: api_key,
            )
        )
        self.files_client = FilesClient(self.working_data_folder_path, verbose)

    def get_datasets(self) -> DatasetFiles:
        download_info = self.dataset_client.download_datasets()
        if self.verbose:
            print(f'Downloading datasets for {download_info["date"]}...')
        files = self.files_client.download_and_extract_datasets(
            download_info["fileUrl"]
        )
        deadline = (
            datetime.fromisoformat(download_info["submissionDeadline"])
            .replace(tzinfo=timezone.utc)
            .astimezone(tz=None)
        )
        duration_remaining = deadline - datetime.now(tz=timezone.utc)
        if self.verbose:
            print(
                f"You have {pretty_timedelta(duration_remaining)} remaining until {deadline.strftime('%d/%m/%Y %H:%M:%S')} to train and submit your predictions for this dataset"
            )
        return {**files, "dataset_date": download_info["date"]}

    def submit_predictions(self, dataset_date: str, submission_file_path: str) -> None:
        upload_info = self.prediction_submission_client.create_submission(
            {
                "datasetDate": dataset_date,
                "filename": os.path.basename(submission_file_path),
            }
        )
        if self.verbose:
            print(
                f'Uploading submission {upload_info["id"]} for {upload_info["datasetDate"]}...'
            )
        self.files_client.upload_submission(
            submission_file_path, upload_info["uploadUrl"]
        )
        if self.verbose:
            print(f'Uploaded submission {upload_info["id"]}')

    def get_past_submissions(self) -> List[Submission]:
        past_submissions = self.prediction_submission_client.list_submissions()

        if not self.verbose:
            return past_submissions["items"]

        print(
            "{:<38} {:<12} {:<20} {:<8} {:<21} {:<20}".format(
                "ID",
                "Dataset Date",
                "Status",
                "Score",
                "Uploaded At",
                "Filename",
            )
        )
        for submission in past_submissions["items"]:
            confidence_score = "N/A"
            if submission.get("confidenceScore") is not None:
                confidence_score = str(round(submission["confidenceScore"], 4))

            uploaded_at = (
                datetime.fromisoformat(submission["uploadedAt"])
                .replace(tzinfo=timezone.utc)
                .astimezone(tz=None)
                .strftime("%Y-%m-%d %H:%M:%S")
            )

            print(
                "{:<38} {:<12} {:<20} {:<8} {:<21} {:<20}".format(
                    submission.get("id"),
                    submission.get("datasetDate"),
                    submission.get("status"),
                    confidence_score,
                    uploaded_at,
                    submission.get("originalFilename", "N/A"),
                )
            )

        return past_submissions["items"]
