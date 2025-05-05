from azure.storage.blob import BlobServiceClient
import os

from app.core.config import settings

blob_service_client = BlobServiceClient.from_connection_string(settings.BLOB_CONNECTION_STRING)
container_name = settings.CONTAINER_NAME


def upload_file_to_blob(file_path: str, file_name: str) -> str:
    try:
        # Connect to the container
        container_client = blob_service_client.get_container_client(container_name)

        # Upload the file
        blob_client = container_client.get_blob_client(file_name)

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        # Return the URL of the uploaded file
        return f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{file_name}"

    except Exception as e:
        raise Exception(f"Error uploading file: {str(e)}")
