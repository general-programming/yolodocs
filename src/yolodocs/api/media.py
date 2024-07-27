from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse, RedirectResponse

from yolodocs import config
from yolodocs.model import File, MediaMetadata
from yolodocs.storage import DBStorage
from yolodocs.storage.s3 import S3Storage

router = APIRouter(prefix="/media", tags=["media"])
db_storage = DBStorage()


@router.get("/")
def list_media():
    media = (
        db_storage.db.query(MediaMetadata).join(File).order_by(File.created_at).all()
    )
    return [x.to_dict() for x in media]


@router.get("/{filename}")
def media_info(filename: str):
    file = db_storage.db.query(File).filter(File.key == filename).first()
    if not file:
        return JSONResponse(
            {"message": "File not found"},
            status_code=404,
        )

    return file.media_metadata.to_dict()


@router.get("/{filename}/transcript")
def transcript(filename: str):
    metadata = db_storage.db.query(File).filter(File.key == filename).first()
    if not metadata:
        return JSONResponse(
            {"message": "File not found"},
            status_code=404,
        )

    return Response(
        metadata.media_metadata.transcript,
        media_type="text/vtt",
    )


@router.get("/{filename}/download")
def download(filename: str) -> bytes:
    # check if file exists on our end
    metadata = db_storage.db.query(File).filter(File.key == filename).first()
    if not metadata:
        return JSONResponse(
            {"message": "File not found"},
            status_code=404,
        )

    # handling for s3
    if isinstance(db_storage.storage, S3Storage):
        presigned_url = db_storage.storage.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": config.S3_BUCKET, "Key": filename},
            ExpiresIn=3600,
        )

        return RedirectResponse(presigned_url)
    else:
        media = db_storage.get(filename)

        return Response(
            media,
            media_type=metadata.mime,
        )
