import requests
import pafy

PREVIEW_URL = "http://img.youtube.com/vi/{}/hqdefault.jpg"
PREVIEW_PATH = "src/shared/previews"


class YoutubePreviewGraber():
    def __init__(
            self,
            video_url: str,
            save_path: str = PREVIEW_PATH
    ) -> None:
        self.video_url = video_url
        self.save_path = save_path

    def get_preview(self) -> str:
        video = pafy.new(self.video_url)
        preview_bytes = requests.get(video.thumb).content
        path = f"{self.save_path}/{self.video_id}.jpg"
        with open(path, "wb") as preview:
            preview.write(preview_bytes)
        return path


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=mVkcWHVB1f4"
    preview_graber = YoutubePreviewGraber(url, PREVIEW_PATH)
    path = preview_graber.get_preview()
    print(path)
