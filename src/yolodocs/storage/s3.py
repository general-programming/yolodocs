import os

import boto3
import boto3.exceptions
import magic
from mypy_boto3_s3 import S3Client

from yolodocs import config
from yolodocs.storage.base import BaseStorage


class S3Storage(BaseStorage):
    def __init__(self):
        self.client: S3Client = boto3.client(
            "s3",
            endpoint_url=config.S3_ENDPOINT_URL,
            aws_access_key_id=config.S3_ACCESS_KEY_ID,
            aws_secret_access_key=config.S3_SECRET_ACCESS_KEY,
            region_name=config.S3_REGION_NAME,
        )

        if not config.S3_BUCKET:
            raise ValueError("S3_BUCKET is not set")

    @property
    def bucket(self):
        return config.S3_BUCKET

    def get(self, key: str) -> bytes:
        obj = self.client.get_object(Bucket=self.bucket, Key=key)
        return obj["Body"].read()

    def put(
        self,
        key: str,
        data: bytes,
        mime: str = None,
    ):
        self.client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=data,
            ContentType=mime,
        )

    def exists(self, key: str):
        try:
            self.client.head_object(self.bucket, key)
            return True
        except self.client.exceptions.NoSuchKey:
            return False
