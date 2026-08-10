---
name: yt-download
description: Download a YouTube video or playlist using this project's `yt` CLI (a yt-dlp wrapper). Use whenever the user pastes a YouTube URL and asks to download, save, archive, or grab a video/playlist. Runs `uv run yt video <url>` or `uv run yt playlist <url>` with flags for output directory, container format, resolution, and subtitle languages — never edit singleVideo.py or playlistVideo.py to change these.
---

# yt-download

This project exposes a `yt` CLI (`src/yt/__init__.py`, backed by `src/yt/singleVideo.py` and
`src/yt/playlistVideo.py`, both built on yt-dlp). Always use the CLI — do not hand-edit those
files to change a URL or setting.

## Decide single video vs playlist

A URL containing `list=` is a playlist; otherwise treat it as a single video.

## Single video

```
uv run yt video "<url>" [-o OUTPUT_DIR] [-f mp4|mkv] [-r RESOLUTION] [-s LANG ...] [--no-subs]
```

- `-o/--output-dir` default `./singleVideos`
- `-f/--format` default `mp4` (or `mkv`)
- `-r/--resolution` default `1080` (max height; e.g. `720`)
- `-s/--subs` default `en` (space-separated language codes, e.g. `-s en es`)
- `--no-subs` skip subtitles entirely

## Playlist

```
uv run yt playlist "<url>" [-o OUTPUT_DIR] [-f mp4|mkv] [-s LANG ...] [--no-auto-subs]
```

- `-o/--output-dir` default `.` (one subfolder per playlist title is created automatically)
- `-f/--format` default `mp4` (or `mkv`)
- `-s/--subs` default `en`
- `--no-auto-subs` don't fall back to YouTube's auto-generated subtitles

## Workflow

1. Identify single video vs playlist from the URL.
2. Use the defaults above unless the user specifies output directory, resolution, format, or
   subtitle languages.
3. Run the command with Bash.
4. Report the resulting output path back to the user.
