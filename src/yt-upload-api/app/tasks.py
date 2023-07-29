import os
from celery import Celery
from uploader.upload import YouTubeUploader


app = Celery('tasks', broker=os.environ.get("CELERY_BROKER_URL"))


@app.task(name="start_upload")
def start_upload(video_id: str):
    uploader = YouTubeUploader(video_id)
    was_video_uploaded, video_id = uploader.upload()
    return was_video_uploaded, video_id
