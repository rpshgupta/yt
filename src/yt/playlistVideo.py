"""
Download a YouTube playlist in 1080p (or best available ≤1080p)
with subtitles, merged into MP4 or MKV.

Requirements:
    pip install yt-dlp
"""

import yt_dlp

def download_playlist(
    playlist_url: str,
    output_format: str = "mp4",          # "mp4" or "mkv"
    subtitle_langs: list[str] = ["en"],  # e.g. ["en", "es"] or ["all"]
    download_auto_subs: bool = True,     # also grab auto-generated subs
    output_dir: str = ".",               # folder where files will be saved
):
    if output_format not in ("mp4", "mkv"):
        raise ValueError("output_format must be 'mp4' or 'mkv'")

    ydl_opts = {
        # Prefer 1080p video + best audio; fall back to best ≤1080p
        "format": (
            "bestvideo[height<=1080]+bestaudio/"
            "best[height<=1080]"
        ),

        # Subtitles
        "writesubtitles": True,
        "writeautomaticsub": download_auto_subs,
        "subtitleslangs": subtitle_langs,
        "embedsubtitles": True,          # embed into the video file
        "subtitlesformat": "srt",        # or "vtt", "ass", etc.

        # Container
        "merge_output_format": output_format,

        # Output template – one folder per playlist
        "outtmpl": f"{output_dir}/%(playlist_title)s/%(playlist_index)02d - %(title)s.%(ext)s",

        # Optional extras
        "ignoreerrors": True,            # continue on individual video errors
        "noplaylist": False,             # ensure playlist is processed
        "quiet": False,
        "progress": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])


