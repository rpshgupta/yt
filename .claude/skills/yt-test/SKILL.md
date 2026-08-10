---
name: yt-test
description: Run this project's pytest suite (unit + integration) and write new test cases for it. Use whenever the user asks to run tests, add tests, check test coverage for a change, or verify a fix/feature in src/yt/ before calling it done. Covers how downloads are tested without hitting the network or YouTube.
---

# yt-test

This project's test suite lives in `tests/` and runs with pytest via `uv`. Never hit the real
network or YouTube in a test — everything mocks the yt-dlp boundary.

## Running tests

```
uv run pytest            # full suite
uv run pytest -q         # quiet
uv run pytest -k video   # filter by name
uv run pytest --lf       # only last failures
```

Run the full suite after any change to `src/yt/` and report pass/fail counts. Treat a failing
test as a bug to fix, not something to delete or skip.

## Layout

- `tests/conftest.py` — defines the `fake_ydl` fixture, which monkeypatches
  `yt_dlp.YoutubeDL` in both `yt.singleVideo` and `yt.playlistVideo` with `FakeYoutubeDL`. Use
  this fixture in every test that goes through `download_video`/`download_playlist` — it
  records the `ydl_opts` dict and downloaded URLs instead of making real requests.
- `tests/unit/` — tests `download_video()` and `download_playlist()` directly: option
  building, defaults, validation, edge cases (no subtitles, no max resolution, custom
  format/resolution/langs).
- `tests/integration/` — drives the real `yt` CLI entry point (`main()` in
  `src/yt/__init__.py`) with `sys.argv` patched, exercising argument parsing through to the
  yt-dlp boundary. Use this level when testing CLI flags/subcommands, not just the underlying
  functions.

## Writing new test cases

When `src/yt/` changes (new flag, new module, new subcommand, bug fix):

1. Add/extend a **unit** test in `tests/unit/` for the function-level behavior (new
   parameter, new default, new validation branch).
2. Add/extend an **integration** test in `tests/integration/test_cli.py` if the change is
   reachable from the CLI (new flag, new subcommand) — assert on the argparse wiring plus the
   resulting `ydl_opts`/downloaded URLs via `fake_ydl`.
3. For a bug fix, first write a test that reproduces the bug and fails, then fix the code and
   confirm it passes.
4. Use `tmp_path` for any `output_dir` argument — never write into the real project
   directories (`singleVideos/`, `easeWithData/`) from a test.
5. Name tests for the behavior being verified (`test_no_max_resolution_uses_best_available`),
   not the implementation (`test_download_video_2`).

Run `uv run pytest` before considering the change done.
