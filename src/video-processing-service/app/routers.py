from fastapi import APIRouter
from tasks import start_processing
from celery.result import AsyncResult

router = APIRouter(
    prefix="/api/v1/processing",
    tags=["processing"],
)


@router.post("/{video_id}")
async def start_processing_video():
    pass
