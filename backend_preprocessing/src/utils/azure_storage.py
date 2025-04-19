from azure.storage.blob import BlobServiceClient
from .config import Config

def get_blob_client(blob_name: str):
    blob_service_client = BlobServiceClient.from_connection_string(Config.AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(Config.AZURE_BLOB_CONTAINER_NAME)
    return container_client.get_blob_client(blob_name)

def read_azure_file(blob_name: str) -> str:
    blob_client = get_blob_client(blob_name)
    download_stream = blob_client.download_blob()
    print(f"Reading file '{blob_name}' from Azure Blob Storage.")
    return download_stream.readall().decode('utf-8')

def write_azure_file(blob_name: str, content: str) -> None:
    blob_client = get_blob_client(blob_name)
    print(f"Writing file '{blob_name}' to Azure Blob Storage.")
    try:
        blob_client.delete_blob()
        print(f"Deleted existing blob '{blob_name}'.")
    except Exception:
        print(f"Blob '{blob_name}' does not exist, proceeding to upload.")
        pass  # Blob may not exist
    blob_client.upload_blob(content.encode('utf-8'), overwrite=True)