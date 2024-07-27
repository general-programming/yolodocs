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
        self.storage.put(key, data, mime, created)

        # update or create
        db_entry = self.db.query(File).filter(File.key == key).first()
        if not db_entry:
            db_entry = File(
                key=key,
            )
            self.db.add(db_entry)

        db_entry.size = len(data)
        db_entry.mime = mime
        db_entry.size = len(data)
        db_entry = created or datetime.now()

        self.db.commit()
