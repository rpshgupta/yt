import pytest


class FakeYoutubeDL:
    """Stand-in for yt_dlp.YoutubeDL that records options/urls instead of hitting the network."""

    instances = []

    def __init__(self, opts):
        self.opts = opts
        self.downloaded = []
        FakeYoutubeDL.instances.append(self)

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        return False

    def download(self, urls):
        self.downloaded.extend(urls)


@pytest.fixture
def fake_ydl(monkeypatch):
    FakeYoutubeDL.instances.clear()
    monkeypatch.setattr("yt.singleVideo.yt_dlp.YoutubeDL", FakeYoutubeDL)
    monkeypatch.setattr("yt.playlistVideo.yt_dlp.YoutubeDL", FakeYoutubeDL)
    return FakeYoutubeDL
