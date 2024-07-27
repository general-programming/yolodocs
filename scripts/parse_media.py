import tempfile

from sqlalchemy import func

from yolodocs.model import File, MediaMetadata
from yolodocs.storage import DBStorage
from yolodocs.tasks.parse import parse_media

db_storage = DBStorage()

# select File objects that do not have a foreign key to MediaMetadata
files = (
    db_storage.db.query(File)
    .filter(File.id.notin_(db_storage.db.query(MediaMetadata.file_id)))
    .all()
)

for file in files:
    print(len(files))
    parse_media(file.key)
