# Synnax Lab SDK

## Installation

```Shell
> pip install synnax-lab-sdk
```

## Usage

```Python
from synnax_lab_sdk.client import SynnaxLabClient

synnax_lab_client = SynnaxLabClient(api_key="your_api_key")
files = synnax_lab_client.get_datasets()
# Train your model and generate predictions
synnax_lab_client.submit_predictions(files["dataset_date"], submissions_path)
```

SDK usage sample file also [available here](https://github.com/synnax-ai/synnax-lab-sdk/blob/master/samples/main.py)

Synnax Lab onboarding manual, including steps to register, download data and make a submission is [available here](https://github.com/synnax-ai/synnax-lab-sdk/blob/master/tutorials/onboarding_manual.ipynb)
