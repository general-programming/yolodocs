from typing import Union

from fastapi import FastAPI

from yolodocs.api import media

app = FastAPI()


app.include_router(media.router)
