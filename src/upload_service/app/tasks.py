from pathlib import Path
from celery import Celery
from uploader.upload import YouTubeUploader

import os


celery = Celery('tasks', broker=os.environ.get("CELERY_BROKER_URL"))


@celery.task(name="start_upload")
def start_upload(video_path: str):
    uploader = YouTubeUploader(video_path)
    was_video_uploaded, video_id = uploader.upload()
    return was_video_uploaded, video_id
