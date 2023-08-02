from pathlib import Path
from edit import VideoEditor
import yt_dlp
import logger
import logging
import json

VIDEO_DIR = Path("src/shared/videos")
PREVIEW_DIR = Path("src/shared/previews")


class VideoPreparation():
    def __init__(
            self,
            video_url: str
    ) -> None:
        self.video_url = video_url
        self.logger = logging.getLogger("prepare")

    def prepare(self) -> str:
        video_path = self.__youtube_download(self.video_url)

        editor = VideoEditor(video_path)
        editor.cut(2, 2)
        editor.apply_effect(speed_factor=1.3)
        editor.render()

        return video_path

    def __youtube_download(self, url) -> str:
        options = dict(
            format='mp4',
            outtmpl=f'{VIDEO_DIR}/%(id)s.%(ext)s',
            writethumbnail=f'{PREVIEW_DIR}/%(id)s.%(ext)s',
        )
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)

        video_id = info.get('id')
        video_file = f'{video_id}.mp4'
        video_path = VIDEO_DIR / video_file

        if video_path.exists():
            self.logger.info(f'Video already exists: {video_path}')
            return video_path

        self.logger.info(f'Downloading: {url}')
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download(url)

        return video_path


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=xxxx"
    preparation = VideoPreparation(url)
    preparation.prepare()
