# eLTER DAR utilities
Utilities for advanced users of eLTER Data Asset Registry
## Installation
Simply run:
```bash
pip install dar-utilities
```
## Usage
The package is designed as a collection of utilities grouped by the role of the user.

For help, run:
```bash
python -m dar_utilities --help
```

### Data Provider (`curator`)
This module contains utilities for creating drafts and submitting datasets to the DAR.
#### Upload module (`upload`)
```
usage: dar_utilities curator upload [-h] -m METADATA -d DATA [-t TOKEN]
options:
  -h, --help            show this help message and exit
  -m METADATA, --metadata METADATA
                        Path to metadata file
  -d DATA, --data DATA  Path to a directory containing data files
  -t TOKEN, --token TOKEN
                        Path to a file containing API token. If not set, the token will be read from the environment variable `DAR_API_TOKEN`.

```

To upload a dataset, run:
```bash
python -m dar_utilities curator upload -m <metadata_file> -d <data_directory>
```


## Usage as Python module
The package can also be used as a Python module. For example, to upload a dataset, you can use the following code:
```python
from dar_utilities.curator.upload import create_dataset_draft, UploadArgs

def main():
    create_dataset_draft(UploadArgs("/path/to/metadata_file", "/path/to/data_directory", "api_token"))

if __name__ == "__main__":
    main()
```