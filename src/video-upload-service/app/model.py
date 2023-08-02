from pydantic import BaseModel


class VideoResponse(BaseModel):
    url: str
