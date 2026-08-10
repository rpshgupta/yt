"""
Download a single YouTube video.

Requirements:
    pip install -U yt-dlp
"""

import yt_dlp
from pathlib import Path


def download_video(
    video_url: str,
    output_dir: str = "./singleVideos",
    output_format: str = "mp4",          # "mp4" or "mkv"
    max_resolution: int = 1080,          # 1080, 720, 480...  None = best available
    subtitle_langs: list[str] | None = ["en"],  # None = no subtitles
):
    """
    Parameters
    ----------
    video_url : str
        Full URL of the video, e.g.
        https://www.youtube.com/watch?v=xxxxxxxxxxx
    output_dir : str
        Folder where the file will be saved.
    output_format : str
        Final container ("mp4" or "mkv").
    max_resolution : int | None
        Prefer height ≤ this value.  None = highest quality.
    subtitle_langs : list[str] | None
        Languages to download & embed.  None disables subtitles.
    """

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    if max_resolution:
        fmt = (
            f"bestvideo[height<={max_resolution}]+bestaudio/"
            f"best[height<={max_resolution}]"
        )
    else:
        fmt = "bestvideo+bestaudio/best"

    ydl_opts = {
        "format": fmt,
        "merge_output_format": output_format,
        "outtmpl": f"{output_dir}/%(title)s [%(id)s].%(ext)s",
        "quiet": False,
        "progress": True,
        "continuedl": True,          # resume if partially downloaded
        "ignoreerrors": False,
    }

    if subtitle_langs:
        ydl_opts.update({
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": subtitle_langs,
            "embedsubtitles": True,
            "subtitlesformat": "srt",
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])


