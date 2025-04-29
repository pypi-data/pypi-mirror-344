import os
import shutil
import uuid
from pathlib import Path
from typing import Optional
import logging

from chainlit.data.storage_clients.base import BaseStorageClient

logger = logging.getLogger(__name__)


class LocalFileStorageClient(BaseStorageClient):
    """
    A storage client that stores files on the local filesystem.
    """

    def __init__(self, base_dir: Optional[str] = None):
        """
        Initialize the local file storage client.

        Args:
            base_dir: The base directory to store files in. If None, defaults to ~/.aki/elements
        """
        if base_dir is None:
            base_dir = str(Path.home() / ".aki" / "elements")

        self.base_dir = os.path.expanduser(base_dir)
        os.makedirs(self.base_dir, exist_ok=True)
        logger.debug(
            f"Initialized LocalFileStorageClient with base directory: {self.base_dir}"
        )

    def upload_file(self, file_path: str, key: Optional[str] = None) -> str:
        """
        Upload a file to local storage.

        Args:
            file_path: The path to the file to upload
            key: Optional key to use for the uploaded file. If None, a UUID will be generated.

        Returns:
            The key of the uploaded file
        """
        try:
            if key is None:
                # Generate a random key using UUID
                key = str(uuid.uuid4())

            # Extract the file extension
            _, ext = os.path.splitext(file_path)

            # Create the destination path
            dest_key = f"{key}{ext}"
            dest_path = os.path.join(self.base_dir, dest_key)

            # Copy the file to the destination
            shutil.copy2(file_path, dest_path)
            logger.info(f"Uploaded file from {file_path} to {dest_path}")

            # Return the key with extension for retrieval
            return dest_key
        except Exception as e:
            logger.error(f"Error uploading file {file_path}: {e}")
            raise

    def delete_file(self, key: str) -> bool:
        """
        Delete a file from local storage.

        Args:
            key: The key of the file to delete

        Returns:
            True if the file was deleted successfully, False otherwise
        """
        try:
            file_path = os.path.join(self.base_dir, key)
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted file: {file_path}")
                return True
            logger.warning(f"File not found for deletion: {file_path}")
            return False
        except Exception as e:
            logger.error(f"Error deleting file {key}: {e}")
            return False

    def get_read_url(self, key: str) -> str:
        """
        Get a URL for reading the file.

        Args:
            key: The key of the file to get the URL for

        Returns:
            The file system path to the file
        """
        file_path = os.path.join(self.base_dir, key)
        logger.debug(f"Generated read URL: {file_path}")
        return file_path
