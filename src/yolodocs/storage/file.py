import os

from yolodocs import config
from yolodocs.storage import BaseStorage


class FileStorage(BaseStorage):
    def __init__(self):
        self.path = config.FILE_STORAGE_FOLDER

    def get(self, key: str):
        file_path = os.path.join(self.path, key)
        with open(file_path, "rb") as f:
            return f

    def put(self, key: str, data: bytes):
        file_path = os.path.join(self.path, key)
        with open(file_path, "wb") as f:
            f.write(data)
