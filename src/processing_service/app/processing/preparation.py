from processing.edit import VideoEditor
from pathlib import Path
from typing import Tuple

import processing.logger
import yt_dlp
import logging
import os

VIDEO_PATH = Path(os.getenv("VIDEO_PATH"))
PREVIEW_PATH = Path(os.getenv("PREVIEW_PATH"))


class VideoPreparation():
    def __init__(
            self,
            video_url: str
    ) -> None:
        self.video_url = video_url
        self.logger = logging.getLogger("prepare")

    def prepare(self) -> Tuple:
        video_path, preview_path, info = self.__youtube_download(self.video_url)

        editor = VideoEditor(video_path)
        editor.cut(2, 2)
        editor.apply_effect(speed_factor=1.3)
        editor.render()

        return video_path, preview_path, info

    def __youtube_download(self, url) -> Path:
        options = dict(
            format='mp4',
            paths={
                'home': f"{VIDEO_PATH}",
                'thumbnail': f"{PREVIEW_PATH}"},
            outtmpl={
                'default': "%(id)s.%(ext)s",
                'thumbnail': "%(id)s.%(ext)s"},
            writethumbnail=True,
            postprocessors=[{
                'format': "jpg",
                'key': "FFmpegThumbnailsConvertor",
                'when': "before_dl"}],
        )
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)

        video_id = info.get('id')
        video_ext = info.get('ext')
        video_file = f'{video_id}.{video_ext}'
        video_path = VIDEO_PATH / video_file
        preview_path = PREVIEW_PATH / f'{video_id}.jpg'

        if video_path.exists():
            self.logger.info(f'Video already exists: {video_path}')
            return video_path

        self.logger.info(f'Downloading: {url}')
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download(url)

        return video_path, preview_path, info


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=xxx"
    preparation = VideoPreparation(url)
    preparation.prepare()
