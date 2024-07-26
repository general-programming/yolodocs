import datetime
import os
import time

from twilio.rest import Client as TwilioClient

from yolodocs.storage import DBStorage
from yolodocs.tasks.download import download_url

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]

db_storage = DBStorage()
twilio = TwilioClient(account_sid, auth_token)

created_before = datetime.datetime.now(datetime.UTC)

while True:
    recordings = twilio.recordings.list(limit=500, date_created_before=created_before)

    for recording in recordings:
        storage_id = f"twilio-{recording.call_sid}-{recording.sid}"

        # skip recordings that are not completed
        if recording.status != "completed":
            print(
                f"Skipping recording {recording.sid} due to status: {recording.status}"
            )
            continue

        download_url.delay(
            storage_id,
            recording.media_url,
            date_created=recording.date_created,
        )

        created_before = min(created_before, recording.date_created)

        print(recording.date_created)

    if len(recordings) == 0:
        break
