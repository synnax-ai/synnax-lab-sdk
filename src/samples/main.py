from synnax_lab_sdk.client import SynnaxLabClient


def main():
    synnax_lab_client = SynnaxLabClient(api_key="your_api_key")
    synnax_lab_client.get_datasets()

    files = synnax_lab_client.get_datasets()

    # TODO: Train your model and generate predictions
    submissions_path = files["sample_submission_path"]

    synnax_lab_client.submit_predictions(submissions_path)

    past_submissions = synnax_lab_client.get_past_submissions()
    print(past_submissions)


if __name__ == "__main__":
    main()
