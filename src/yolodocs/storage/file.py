import os

from yolodocs import config
from yolodocs.storage.base import BaseStorage


class FileStorage(BaseStorage):
    def __init__(self):
        self.path = config.FILE_STORAGE_FOLDER

    def get(self, key: str) -> bytes:
        file_path = os.path.join(self.path, key)
        with open(file_path, "rb") as f:
            return f.read()

    def put(
        self,
        key: str,
        data: bytes,
        mime: str,
    ):
        file_path = os.path.join(self.path, key)
        with open(file_path, "wb") as f:
            f.write(data)

    def exists(self, key: str):
        file_path = os.path.join(self.path, key)
        return os.path.exists(file_path)
