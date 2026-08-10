import sys

import pytest

from yt import main


def run_cli(monkeypatch, args):
    monkeypatch.setattr(sys, "argv", ["yt", *args])
    main()


def test_video_subcommand_downloads_with_defaults(fake_ydl, monkeypatch, tmp_path):
    out_dir = tmp_path / "videos"

    run_cli(monkeypatch, ["video", "https://youtu.be/abc123", "-o", str(out_dir)])

    assert out_dir.is_dir()
    ydl = fake_ydl.instances[0]
    assert ydl.downloaded == ["https://youtu.be/abc123"]
    assert ydl.opts["merge_output_format"] == "mp4"
    assert ydl.opts["subtitleslangs"] == ["en"]


def test_video_subcommand_no_subs_flag(fake_ydl, monkeypatch, tmp_path):
    run_cli(monkeypatch, ["video", "https://youtu.be/abc123", "-o", str(tmp_path), "--no-subs"])

    assert "writesubtitles" not in fake_ydl.instances[0].opts


def test_video_subcommand_custom_flags(fake_ydl, monkeypatch, tmp_path):
    run_cli(
        monkeypatch,
        [
            "video", "https://youtu.be/abc123",
            "-o", str(tmp_path),
            "-f", "mkv",
            "-r", "720",
            "-s", "en", "es",
        ],
    )

    opts = fake_ydl.instances[0].opts
    assert opts["merge_output_format"] == "mkv"
    assert "height<=720" in opts["format"]
    assert opts["subtitleslangs"] == ["en", "es"]


def test_playlist_subcommand_downloads_with_defaults(fake_ydl, monkeypatch, tmp_path):
    run_cli(monkeypatch, ["playlist", "https://youtube.com/playlist?list=XYZ", "-o", str(tmp_path)])

    ydl = fake_ydl.instances[0]
    assert ydl.downloaded == ["https://youtube.com/playlist?list=XYZ"]
    assert ydl.opts["writeautomaticsub"] is True


def test_playlist_subcommand_no_auto_subs_flag(fake_ydl, monkeypatch, tmp_path):
    run_cli(monkeypatch, ["playlist", "https://youtube.com/playlist?list=XYZ", "-o", str(tmp_path), "--no-auto-subs"])

    assert fake_ydl.instances[0].opts["writeautomaticsub"] is False


def test_cli_requires_a_subcommand(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["yt"])

    with pytest.raises(SystemExit):
        main()


def test_cli_rejects_unknown_format(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "argv", ["yt", "video", "https://youtu.be/abc123", "-f", "avi"])

    with pytest.raises(SystemExit):
        main()
