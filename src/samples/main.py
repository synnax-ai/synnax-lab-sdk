from synnax_lab_sdk.client import SynnaxLabClient


def main():
    synnax_lab_client = SynnaxLabClient(api_key="your_api_key")
    synnax_lab_client.get_datasets()


if __name__ == "__main__":
    main()
