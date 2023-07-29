import os
from celery import Celery


app = Celery('tasks', broker=os.environ.get("CELERY_BROKER_URL"))


@app.task(name="start_processing")
def start_processing(video_id: str):
    pass
