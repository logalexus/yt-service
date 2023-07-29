from fastapi import APIRouter
from tasks import start_upload
from celery.result import AsyncResult

router = APIRouter(
    prefix="/api/v1/processing",
    tags=["upload"],
)


@router.post("/{video_id}")
async def start_processing_video():
    pass
