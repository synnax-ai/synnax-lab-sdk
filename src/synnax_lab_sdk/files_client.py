import os
import tarfile
from pathlib import Path
from typing import TypedDict

import requests
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper


class DatasetFilePaths(TypedDict):
    x_train_path: str
    targets_train_path: str
    x_forward_looking_path: str
    macro_train_path: str
    macro_forward_looking_path: str
    sample_submission_path: str
    data_dictionary_path: str


class FilesClient:
    def __init__(self, working_data_folder_path: str, show_progress: bool = False):
        self.working_data_folder_path = working_data_folder_path
        self.show_progress = show_progress

    def download_and_extract_datasets(self, download_url: str) -> DatasetFilePaths:
        download_file_path = os.path.join(
            self.working_data_folder_path, "datasets.tar.gz"
        )
        extracted_folder_path = os.path.join(self.working_data_folder_path, "datasets")

        Path(self.working_data_folder_path).mkdir(parents=True, exist_ok=True)
        Path(extracted_folder_path).mkdir(parents=True, exist_ok=True)

        with requests.get(download_url, stream=True) as response:
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))
            chunk_size = 1024
            with tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                disable=not self.show_progress,
            ) as progress_bar:
                with open(download_file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size):
                        progress_bar.update(len(chunk))
                        file.write(chunk)

        with tarfile.open(download_file_path) as tar:
            tar.extractall(extracted_folder_path)

        return {
            "x_train_path": os.path.join(extracted_folder_path, "X_train.csv"),
            "targets_train_path": os.path.join(
                extracted_folder_path, "targets_train.csv"
            ),
            "x_forward_looking_path": os.path.join(
                extracted_folder_path, "X_forward_looking.csv"
            ),
            "macro_train_path": os.path.join(extracted_folder_path, "macro_train.csv"),
            "macro_forward_looking_path": os.path.join(
                extracted_folder_path, "macro_forward_looking.csv"
            ),
            "sample_submission_path": os.path.join(
                extracted_folder_path, "sample_submission.csv"
            ),
            "data_dictionary_path": os.path.join(
                extracted_folder_path, "data_dictionary.txt"
            ),
        }

    def upload_submission(self, submission_file_path: str, upload_url: str) -> None:
        file_size = os.stat(submission_file_path).st_size
        with open(submission_file_path, "rb") as file:
            with tqdm(
                total=file_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                disable=not self.show_progress,
            ) as progress_bar:
                wrapped_file = CallbackIOWrapper(progress_bar.update, file, "read")
                requests.put(upload_url, data=wrapped_file)
