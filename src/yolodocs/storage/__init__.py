class BaseStorage:
    def __init__(self):
        pass

    def get(self, key: str):
        raise NotImplementedError

    def put(self, key: str, data: bytes):
        raise NotImplementedError
