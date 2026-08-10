import pytest

from yt.playlistVideo import download_playlist


def test_builds_default_options(fake_ydl, tmp_path):
    download_playlist("https://youtube.com/playlist?list=XYZ", output_dir=str(tmp_path))

    ydl = fake_ydl.instances[0]
    assert ydl.downloaded == ["https://youtube.com/playlist?list=XYZ"]
    opts = ydl.opts
    assert opts["merge_output_format"] == "mp4"
    assert opts["writeautomaticsub"] is True
    assert opts["subtitleslangs"] == ["en"]
    assert "%(playlist_title)s" in opts["outtmpl"]


def test_rejects_unsupported_output_format(fake_ydl):
    with pytest.raises(ValueError):
        download_playlist("https://youtube.com/playlist?list=XYZ", output_format="avi")


def test_disabling_auto_subs_is_reflected_in_options(fake_ydl, tmp_path):
    download_playlist(
        "https://youtube.com/playlist?list=XYZ",
        output_dir=str(tmp_path),
        download_auto_subs=False,
    )

    assert fake_ydl.instances[0].opts["writeautomaticsub"] is False


def test_custom_subtitle_langs_and_format(fake_ydl, tmp_path):
    download_playlist(
        "https://youtube.com/playlist?list=XYZ",
        output_dir=str(tmp_path),
        output_format="mkv",
        subtitle_langs=["en", "fr"],
    )

    opts = fake_ydl.instances[0].opts
    assert opts["merge_output_format"] == "mkv"
    assert opts["subtitleslangs"] == ["en", "fr"]
