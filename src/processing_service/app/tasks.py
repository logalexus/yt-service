import os
from celery import Celery
from processing.preparation import VideoPreparation


celery = Celery('tasks', broker=os.environ.get("CELERY_BROKER_URL"))


@celery.task(name="start_processing")
def start_processing(video_url: str):
    preparation = VideoPreparation(video_url)
    video_path, preview_path, info = preparation.prepare()
