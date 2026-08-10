# yt

A small command-line tool for downloading YouTube videos and playlists (video + subtitles,
merged into a single MP4/MKV file) built on top of [`yt-dlp`](https://github.com/yt-dlp/yt-dlp).

## Table of contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Download a single video](#download-a-single-video)
  - [Download a playlist](#download-a-playlist)
- [Project structure](#project-structure)
- [How downloads are built](#how-downloads-are-built)
- [Testing](#testing)
- [Claude Code skills](#claude-code-skills)
- [Downloaded media & .gitignore](#downloaded-media--gitignore)
- [Development](#development)

## Features

- Download a single video or an entire playlist from the command line — no code edits needed.
- Video + audio merged into one file, container format selectable (`mp4` or `mkv`).
- Subtitles (manual and/or auto-generated) downloaded and embedded, language(s) selectable.
- Resolution cap for single videos (defaults to best available ≤ 1080p).
- Resumable downloads (`continuedl`) for single videos.
- Playlists are saved one subfolder per playlist, files numbered by playlist index.
- Fully unit- and integration-tested without ever touching the network.

## Requirements

- Python ≥ 3.12
- [`uv`](https://docs.astral.sh/uv/) for dependency management and running the CLI/tests
- `ffmpeg` available on `PATH` (required by `yt-dlp` to merge/embed video, audio, and subtitles)

## Installation

```bash
git clone https://github.com/rpshgupta/yt.git
cd yt
uv sync
```

`uv sync` creates a `.venv/`, installs runtime dependencies (`requests`, `yt-dlp`) and dev
dependencies (`pytest`), and installs this package (with its `yt` console script) in editable
mode.

## Usage

The package installs a `yt` command with two subcommands: `video` and `playlist`. Run
everything through `uv run` (or activate `.venv` and call `yt` directly).

```
uv run yt --help
uv run yt video --help
uv run yt playlist --help
```

### Download a single video

```bash
uv run yt video "<video-url>" [-o OUTPUT_DIR] [-f mp4|mkv] [-r RESOLUTION] [-s LANG [LANG ...]] [--no-subs]
```

| Flag | Default | Description |
|---|---|---|
| `url` (positional) | — | Full video URL, e.g. `https://www.youtube.com/watch?v=xxxxxxxxxxx` |
| `-o`, `--output-dir` | `./singleVideos` | Folder the file is saved into |
| `-f`, `--format` | `mp4` | Output container: `mp4` or `mkv` |
| `-r`, `--resolution` | `1080` | Maximum video height; best available ≤ this value (e.g. `-r 720`) |
| `-s`, `--subs` | `en` | One or more subtitle language codes, e.g. `-s en es` |
| `--no-subs` | off | Skip subtitles entirely |

Example — download a video at 720p in MKV with English and Spanish subtitles into `./out`:

```bash
uv run yt video "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o ./out -f mkv -r 720 -s en es
```

Output filenames follow `%(title)s [%(id)s].%(ext)s`.

### Download a playlist

```bash
uv run yt playlist "<playlist-url>" [-o OUTPUT_DIR] [-f mp4|mkv] [-s LANG [LANG ...]] [--no-auto-subs]
```

| Flag | Default | Description |
|---|---|---|
| `url` (positional) | — | Full playlist URL, e.g. `https://www.youtube.com/playlist?list=xxxxxxxxxxx` |
| `-o`, `--output-dir` | `.` | Parent folder; a subfolder named after the playlist title is created inside it |
| `-f`, `--format` | `mp4` | Output container: `mp4` or `mkv` |
| `-s`, `--subs` | `en` | One or more subtitle language codes, e.g. `-s en es` |
| `--no-auto-subs` | off | Don't fall back to YouTube's auto-generated subtitles |

Example — download a playlist into `./courses`, keeping only manually-authored English subs:

```bash
uv run yt playlist "https://www.youtube.com/playlist?list=PLxxxxxxxxxxxxxxxxxx" -o ./courses --no-auto-subs
```

Every video in the playlist that fails to download is skipped (`ignoreerrors: True`) so one
broken video doesn't stop the rest. Output filenames follow
`<output-dir>/<playlist title>/<playlist index> - <title>.<ext>`.

## Project structure

```
.
├── src/yt/
│   ├── __init__.py        # `yt` CLI entry point (argparse: video / playlist subcommands)
│   ├── singleVideo.py     # download_video() — single-video download logic
│   └── playlistVideo.py   # download_playlist() — playlist download logic
├── tests/
│   ├── conftest.py        # fake_ydl fixture: mocks the yt-dlp network boundary
│   ├── unit/               # tests download_video()/download_playlist() directly
│   └── integration/        # tests the `yt` CLI end-to-end (argparse → yt-dlp boundary)
├── .claude/skills/
│   ├── yt-download/        # skill: run downloads via the CLI instead of editing source
│   └── yt-test/            # skill: run/extend the pytest suite
├── pyproject.toml
└── uv.lock
```

## How downloads are built

Both download functions build a `yt_dlp.YoutubeDL` options dict and hand it a single URL:

- **`download_video`** (`src/yt/singleVideo.py`): creates `output_dir` if missing, picks a
  format string capped at `max_resolution` (or `bestvideo+bestaudio/best` if
  `max_resolution=None`), and — if `subtitle_langs` is truthy — enables subtitle download,
  auto-sub fallback, and embedding in `srt` format.
- **`download_playlist`** (`src/yt/playlistVideo.py`): validates `output_format` is `mp4` or
  `mkv`, always requests subtitles for the given `subtitle_langs`
  (`download_auto_subs` controls whether auto-generated subs are used as a fallback), and sets
  `ignoreerrors=True` so a single bad video doesn't abort the whole playlist.

The CLI (`src/yt/__init__.py`) is a thin argparse layer that maps `video`/`playlist` flags onto
the keyword arguments of these two functions — it holds no download logic of its own.

## Testing

The suite uses `pytest` and never hits the network: `tests/conftest.py` defines a `fake_ydl`
fixture that monkeypatches `yt_dlp.YoutubeDL` (in both `yt.singleVideo` and
`yt.playlistVideo`) with an in-memory `FakeYoutubeDL` that records the options dict and the
URLs passed to `.download()` instead of making real requests.

```bash
uv run pytest            # full suite
uv run pytest -q         # quiet
uv run pytest -k video   # filter by name
uv run pytest --lf       # only last failures
```

- **`tests/unit/`** — tests `download_video()` and `download_playlist()` directly: default
  option building, subtitle handling, resolution/format validation, and edge cases (no
  subtitles, no max resolution, custom format/resolution/languages).
- **`tests/integration/`** — drives the real `yt` CLI entry point (`main()`) with `sys.argv`
  patched, exercising argument parsing through to the `yt_dlp.YoutubeDL` boundary — this is
  where CLI flags and subcommand wiring are verified, as opposed to the underlying functions.

As of this writing the suite has 15 tests, all passing, with no network or filesystem writes
outside `tmp_path`.

## Claude Code skills

This repo ships two [Claude Code](https://claude.com/claude-code) project skills under
`.claude/skills/` so routine work doesn't require editing source files by hand:

- **`yt-download`** — given a YouTube URL, runs `uv run yt video ...` or
  `uv run yt playlist ...` with the right flags instead of hardcoding a URL/config inside
  `singleVideo.py`/`playlistVideo.py`.
- **`yt-test`** — runs the pytest suite and adds new unit/integration test cases (using the
  `fake_ydl` fixture and `tmp_path`) whenever `src/yt/` changes.

## Downloaded media & .gitignore

Downloaded videos, audio, and subtitle files are never committed. `.gitignore` excludes them
by extension (not by folder name), so any playlist/video output directory — regardless of its
name — is automatically kept out of git as long as it only contains:

```
*.mp4 *.mkv *.webm *.m4a *.mp3 *.srt *.vtt *.part *.ytdl
```

## Development

```bash
uv sync                  # install/update dependencies
uv run yt --help          # run the CLI
uv run pytest             # run the test suite
uv add <package>          # add a runtime dependency
uv add --dev <package>    # add a dev-only dependency
```

When changing `src/yt/`, add corresponding tests (see [Testing](#testing) and the `yt-test`
skill) before considering a change complete.
