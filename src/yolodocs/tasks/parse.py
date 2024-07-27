import io
import math
import tempfile

from pymediainfo import MediaInfo
from pywhispercpp.model import Model as WhisperModel
from pywhispercpp.utils import to_timestamp

from yolodocs.model import File, MediaMetadata, MediaType
from yolodocs.storage import DBStorage
from yolodocs.tasks import app

# TODO: Have the model be set in the config
model = WhisperModel("models/ggml-large-v3.bin", n_threads=8)
print(model.system_info())
db_storage = DBStorage()


def parse_vtt(segments):
    result = ""

    for i in range(len(segments)):
        seg = segments[i]
        result += f"{i+1}\n"
        result += f"{to_timestamp(seg.t0, separator=',')} --> {to_timestamp(seg.t1, separator=',')}\n"
        result += f"{seg.text}\n\n"

    return result


@app.task(
    autoretry_for=(Exception,),
    retry_backoff=2,
    max_retries=10,
)
def parse_media(key: str):
    db_row = db_storage.db.query(File).filter(File.key == key).first()
    if not db_row:
        print(f"Could not find file with key {key}")
        return

    data = db_storage.get(key)

    with tempfile.NamedTemporaryFile(delete_on_close=False) as f:
        f.write(data)
        f.flush()
        f.close()

        # parse media info
        media_info = MediaInfo.parse(f.name)
        # TODO: Is track 0 the best track to use?
        media_length_ms = media_info.tracks[0].duration
        # DEBUG
        print(f"START {key} {media_length_ms / 1000}s {db_row.size} bytes")

        # get tokens
        parsed_results = model.transcribe(f.name)
        parsed_vtt = parse_vtt(parsed_results)

        # store in db
        metadata_row = (
            db_storage.db.query(MediaMetadata)
            .filter(MediaMetadata.file_id == db_row.id)
            .first()
        )
        if not metadata_row:
            metadata_row = MediaMetadata(file_id=db_row.id)
            db_storage.db.add(metadata_row)

        # TODO: Determine media type later
        metadata_row.media_type = MediaType.audio
        metadata_row.transcript = parsed_vtt
        metadata_row.media_length_ms = media_length_ms
        metadata_row.media_length = math.ceil(media_length_ms / 1000)

        # DEBUG
        print(f"END {key} {media_length_ms / 1000}s {db_row.size} bytes {parsed_vtt}")

        db_storage.db.commit()
