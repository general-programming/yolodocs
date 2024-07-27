from datetime import datetime

from yolodocs import config
from yolodocs.model import File, sm
from yolodocs.storage.file import FileStorage
from yolodocs.storage.s3 import S3Storage


def get_storage():
    if config.FILE_STORAGE_TYPE == "file":
        return FileStorage()
    elif config.FILE_STORAGE_TYPE == "s3":
        return S3Storage()

    raise KeyError(f"Unknown storage type: {config.FILE_STORAGE_TYPE}")


class DBStorage:
    def __init__(self):
        self.storage = get_storage()
        self.db = sm()

    def exists(self, key: str):
        db_entry = self.db.query(File).filter(File.key == key).first()
        return db_entry is not None

    def get(self, key: str) -> bytes:
        return self.storage.get(key)

    def put(
        self,
        key: str,
        data: bytes,
        mime: str = None,
        created: datetime = None,
    ):
        if self.exists(key):
            raise KeyError(f"File with key {key} already exists")

        # TODO: created at
        self.storage.put(key, data, mime)

        db_entry = File(
            key=key,
            created_at=created or datetime.now(),
            size=len(data),
            mime=mime,
        )
        self.db.add(db_entry)
        self.db.commit()
