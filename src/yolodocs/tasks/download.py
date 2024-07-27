import mimetypes
from datetime import datetime

import magic
import requests

from yolodocs.storage import DBStorage
from yolodocs.tasks import app

db_storage = DBStorage()


@app.task(
    autoretry_for=(Exception,),
    retry_backoff=2,
    max_retries=10,
)
def download_url(
    key: str,
    url: str,
    date_created: datetime = None,
):
    r = requests.get(url)
    r.raise_for_status()
    mime_type = magic.from_buffer(r.content, mime=True)

    db_storage.put(
        key,
        r.content,
        mime=mime_type,
        created=date_created,
    )

    print(f"Downloaded {key} ({url}): {mime_type} {len(r.content)} bytes")
