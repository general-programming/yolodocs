import os

# storage type
FILE_STORAGE_TYPE = os.environ.get("STORAGE_TYPE", "file")

# flatfile storage
FILE_STORAGE_FOLDER = os.environ.get("STORAGE_FOLDER", "files")

# s3 storage
S3_BUCKET = os.environ.get("S3_BUCKET", None)
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL", None)
S3_ACCESS_KEY_ID = os.environ.get("S3_ACCESS_KEY_ID", None)
S3_SECRET_ACCESS_KEY = os.environ.get("S3_SECRET_ACCESS_KEY", None)
S3_REGION_NAME = os.environ.get("S3_REGION_NAME", "us-east-1")
