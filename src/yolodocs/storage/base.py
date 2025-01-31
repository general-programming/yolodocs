from datetime import datetime


class BaseStorage:
    def __init__(self):
        pass

    def get(self, key: str) -> bytes:
        raise NotImplementedError

    def put(
        self,
        key: str,
        data: bytes,
        mime: str = None,
        created: datetime = None,
    ):
        raise NotImplementedError

    def exists(self, key: str):
        raise NotImplementedError
