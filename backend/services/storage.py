"""
Storage service for uploading and managing design images
"""
import os
import tempfile
import uuid
from pathlib import Path
from fastapi import UploadFile
import aiofiles
from backend.config import MAX_UPLOAD_SIZE_MB

# Local storage for development
UPLOAD_DIR = Path(tempfile.gettempdir()) / "designaudit_uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class StorageService:
    """Handle file storage operations"""

    @staticmethod
    async def save_upload(file: UploadFile) -> tuple[str, str]:
        """
        Save uploaded file and return (local_path, storage_url)
        """
        # Validate file size
        contents = await file.read()
        if len(contents) > MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            raise ValueError(f"File exceeds maximum size of {MAX_UPLOAD_SIZE_MB}MB")

        # Generate unique filename
        file_ext = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        file_path = UPLOAD_DIR / unique_filename

        # Save file
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(contents)

        # Return local path and URL
        storage_url = f"file://{file_path}"
        return str(file_path), storage_url

    @staticmethod
    async def delete_file(file_path: str) -> bool:
        """Delete a file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception as e:
            print(f"Error deleting file: {e}")
        return False

    @staticmethod
    async def read_file(file_path: str) -> bytes:
        """Read file contents"""
        async with aiofiles.open(file_path, "rb") as f:
            return await f.read()
