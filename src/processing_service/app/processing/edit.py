from pathlib import Path
from moviepy.editor import VideoFileClip
from moviepy.video.fx.speedx import speedx

import os
import platform


class VideoEditor():
    def __init__(self, video_path: Path) -> None:
        self.clip = VideoFileClip(str(video_path))
        self.video_path = video_path

    def cut(self, start: int, from_end: int) -> None:
        self.clip = self.clip.subclip(start, self.clip.duration - from_end)

    def apply_effect(self, speed_factor: float = 1) -> None:
        self.clip = speedx(self.clip, speed_factor)

    def render(self, save_path: Path = None):
        temp_path = self.video_path.parent / ("temp_" + self.video_path.name)

        if (save_path is None):
            save_path = temp_path

        self.clip.write_videofile(str(save_path),
                                  preset="ultrafast",
                                  fps=30,
                                  threads=1,
                                  codec="libx264",
                                  temp_audiofile=False)
        self.clip.close()

        os.remove(self.video_path)
        os.rename(temp_path, self.video_path)

        return self.video_path


if __name__ == "__main__":
    editor = VideoEditor(Path("/shared/videos/video.mp4"))
    editor.cut(2, 2)
    editor.apply_effect(1.1)
    editor.render()
