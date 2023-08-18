from pydantic import BaseModel


class UploadModel(BaseModel):
    video_path: str
