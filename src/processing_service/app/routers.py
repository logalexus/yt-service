from fastapi import APIRouter, HTTPException, status
from tasks import start_processing
from celery.result import AsyncResult
from model import ProcessingModel

router = APIRouter(
    prefix="/api/v1/processing",
    tags=["processing"],
)


@router.get("/status/{task_id}")
async def get_status(task_id):
    task_result = AsyncResult(task_id)
    return {"task_status": task_result.status}


@router.get("/result/{task_id}")
async def get_result(task_id):
    task_result = AsyncResult(task_id)
    return {"task_status": task_result.result}


@router.post("/")
async def start_processing_video(model: ProcessingModel):
    try:
        if not model.video_url:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Video url is empty")
        task = start_processing.apply_async(args=[model.video_url], queue="processing")
    except Exception as ex:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
    return {"task_id": task.id}
    
