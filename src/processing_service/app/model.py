from pydantic import BaseModel


class ProcessingModel(BaseModel):
    video_url: str
