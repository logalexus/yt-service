from fastapi import APIRouter
from tasks import start_upload
from celery.result import AsyncResult

router = APIRouter(
    prefix="/api/v1/upload",
    tags=["upload"],
)


@router.get("/status/{task_id}")
async def get_status(task_id):
    task_result = AsyncResult(task_id)
    return {"task_status": task_result.status}


@router.get("/result/{task_id}")
async def get_result(task_id):
    task_result = AsyncResult(task_id)
    return {"task_status": task_result.result}


@router.post("/{video_id}")
async def create_item(video_id: str):
    task = start_upload.delay(video_id)
    return {"task_id": task.id}
