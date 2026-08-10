from yt.singleVideo import download_video


def test_builds_default_options_and_creates_output_dir(fake_ydl, tmp_path):
    out_dir = tmp_path / "videos"

    download_video("https://youtu.be/abc123", output_dir=str(out_dir))

    assert out_dir.is_dir()
    ydl = fake_ydl.instances[0]
    assert ydl.downloaded == ["https://youtu.be/abc123"]
    assert ydl.opts["merge_output_format"] == "mp4"
    assert "height<=1080" in ydl.opts["format"]
    assert ydl.opts["writesubtitles"] is True
    assert ydl.opts["subtitleslangs"] == ["en"]


def test_no_subtitle_langs_omits_subtitle_options(fake_ydl, tmp_path):
    download_video("https://youtu.be/abc123", output_dir=str(tmp_path), subtitle_langs=None)

    opts = fake_ydl.instances[0].opts
    assert "writesubtitles" not in opts
    assert "subtitleslangs" not in opts


def test_no_max_resolution_uses_best_available(fake_ydl, tmp_path):
    download_video("https://youtu.be/abc123", output_dir=str(tmp_path), max_resolution=None)

    assert fake_ydl.instances[0].opts["format"] == "bestvideo+bestaudio/best"


def test_custom_format_resolution_and_subtitle_langs(fake_ydl, tmp_path):
    download_video(
        "https://youtu.be/abc123",
        output_dir=str(tmp_path),
        output_format="mkv",
        max_resolution=720,
        subtitle_langs=["en", "es"],
    )

    opts = fake_ydl.instances[0].opts
    assert opts["merge_output_format"] == "mkv"
    assert "height<=720" in opts["format"]
    assert opts["subtitleslangs"] == ["en", "es"]
