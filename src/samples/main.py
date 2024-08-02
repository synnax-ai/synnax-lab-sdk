from synnax_lab_sdk.client import SynnaxLabClient


def main():
    synnax_lab_client = SynnaxLabClient(api_key="your_api_key")

    files = synnax_lab_client.get_datasets()

    # TODO: Train your model and generate predictions
    submissions_path = files["sample_submission_path"]

    synnax_lab_client.submit_predictions(files["dataset_date"], submissions_path)

    synnax_lab_client.get_past_submissions()


if __name__ == "__main__":
    main()
