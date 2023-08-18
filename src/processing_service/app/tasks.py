import os
from celery import Celery
from processing.preparation import VideoPreparation

import requests
import json

celery = Celery('tasks', broker=os.environ.get("CELERY_BROKER_URL"))


UPLOAD_API = os.getenv("UPLOAD_API")


@celery.task(name="start_processing")
def start_processing(video_url: str):
    preparation = VideoPreparation(video_url)
    video_path, preview_path, info = preparation.prepare()
    data = {"video_path" : str(video_path)}
    json_data = json.dumps(data)
    requests.post(UPLOAD_API, data=json_data)
