from yolodocs.model import File, MediaMetadata
from yolodocs.storage import DBStorage

db_storage = DBStorage()

for metadata in (
    db_storage.db.query(MediaMetadata).where(MediaMetadata.transcript != "").all()
):
    if "WEBVTT" not in metadata.transcript:
        new_transcript = "WEBVTT\n\n"

        for line in metadata.transcript.split("\n\n"):
            lines = line.split("\n", 2)
            if len(lines) != 3:
                continue
            new_transcript += lines[1].replace(",", ".") + "\n" + lines[2] + "\n\n"

        metadata.transcript = new_transcript

    db_storage.db.commit()
