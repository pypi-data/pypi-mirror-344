import argparse
import json
import logging
import os
import pathlib
from typing import Any
from requests_toolbelt import sessions

def create_dataset_draft(upload_args: "UploadArgs") -> str:
    """
    Create a dataset draft in the eLTER DAR.

    Args:
        upload_args (UploadArgs): Arguments for uploading the dataset.
    Returns:
        str: The ID of the created dataset draft.
    Raises:
        ValueError: If the dataset draft creation or file upload fails.
    """
    # Prepare the session
    session = sessions.BaseUrlSession(base_url="https://dar.elter-ri.eu")
    session.headers.update({"Authorization": f"Bearer {upload_args.token}"})
    session.headers.update({"Content-Type": "application/json"})

    # Create the dataset draft
    with open(upload_args.metadata_path, "r") as file:
        metadata = json.load(file)

        request_object = {
            "parent": {
                "communities": {
                    "default": "elter"
                }
            },
            "metadata": metadata,
            "files": {
                "enabled": True
            },
            "externalWorkflow": {
                "defaultWorkflowTemplateId": "basic-ingest"
            },
        }

        # Send the request to create the dataset draft
        response = session.post("/api/datasets", json=request_object)

        if not response.ok:
            logging.error(f"Failed to create dataset draft: {response.status_code} - {response.text}")
            raise ValueError("Failed to create dataset draft.")

    created_draft = response.json()
    draft_id = created_draft["id"]

    logging.info(f"Dataset draft created successfully with ID: {draft_id}")
    # Upload the files

    files_to_upload = []
    for root, _, files in os.walk(upload_args.data_dir_path):
        for file_name in files:
            files_to_upload.append(pathlib.Path(os.path.join(root, file_name)))


    if not files_to_upload:
        logging.warning("No files found to upload.")
        return draft_id

    # Register the files for upload
    file_registration_payload = [{
        "key": file.name,
    } for file in files_to_upload]

    response = session.post(f"/api/datasets/{draft_id}/draft/files", json=file_registration_payload)
    if not response.ok:
        logging.error(f"Failed to register files for upload: {response.status_code} - {response.text}")
        raise ValueError("Failed to register files for upload.")

    # Upload file content
    file_upload_session = sessions.BaseUrlSession(base_url="https://dar.elter-ri.eu")
    file_upload_session.headers.update({"Authorization": f"Bearer {upload_args.token}"})
    file_upload_session.headers.update({"Content-Type": "application/octet-stream"})

    for file in files_to_upload:
        with open(file, "rb") as file_content:
            response = file_upload_session.put(f"/api/datasets/{draft_id}/draft/files/{file.name}/content", data=file_content)
            if not response.ok:
                logging.error(f"Failed to upload file {file.name}: {response.status_code} - {response.text}")
                raise ValueError(f"Failed to upload file {file.name}.")


    # Commit uploaded files
    for file in files_to_upload:
        response = session.post(f"/api/datasets/{draft_id}/draft/files/{file.name}/commit")
        if not response.ok:
            logging.error(f"Failed to commit file {file.name}: {response.status_code} - {response.text}")
            raise ValueError(f"Failed to commit file {file.name}.")

    logging.info(f"Files uploaded and committed successfully for dataset draft ID: {draft_id}")

    return draft_id


def _configure_argparse_subparser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-m", "--metadata", type=str, required=True, help="Path to metadata file")
    parser.add_argument("-d", "--data", type=str, required=True, help="Path to a directory containing data files")
    parser.add_argument("-t", "--token", type=str, required=False, help="Path to a file containing API token. If not set, the token will be read from the environment variable `DAR_API_TOKEN`.")

    parser.set_defaults(func=__parse_args_and_upload)

    return parser

def __parse_args_and_upload(args: Any) -> None:
    args = __parse_arguments(args)
    create_dataset_draft(args)


def __parse_arguments(args: Any) -> "UploadArgs":
    if args.token is None:
        token = os.environ.get("DAR_API_TOKEN")
        if token is None:
            logging.error("API token must be provided either as a command line argument or via the environment variable `DAR_API_TOKEN`.")
            raise ValueError("API token is required.")
    else:
        if not os.path.isfile(args.token):
            logging.error(f"Token file does not exist: {args.token}")
            raise ValueError("Token file does not exist.")

        with open(args.token) as file:
            token = file.read().strip()

    if not os.path.isfile(args.metadata):
        logging.error(f"Metadata file does not exist: {args.metadata}")
        raise ValueError("Metadata file does not exist.")

    if not os.path.isdir(args.data):
        logging.error(f"Data directory does not exist: {args.data}")
        raise ValueError("Metadata file does not exist.")


    return UploadArgs(token=token, metadata=args.metadata, data=args.data)



class UploadArgs:
    def __init__(self, metadata: str, data: str, token: str):
        self.metadata_path = metadata
        self.data_dir_path = data
        self.token = token