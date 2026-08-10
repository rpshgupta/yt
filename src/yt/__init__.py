import argparse

from yt.playlistVideo import download_playlist
from yt.singleVideo import download_video


def main() -> None:
    parser = argparse.ArgumentParser(prog="yt", description="Download YouTube videos/playlists via yt-dlp")
    sub = parser.add_subparsers(dest="command", required=True)

    video_p = sub.add_parser("video", help="Download a single video")
    video_p.add_argument("url")
    video_p.add_argument("-o", "--output-dir", default="./singleVideos")
    video_p.add_argument("-f", "--format", default="mp4", choices=["mp4", "mkv"])
    video_p.add_argument("-r", "--resolution", type=int, default=1080)
    video_p.add_argument("-s", "--subs", nargs="*", default=["en"])
    video_p.add_argument("--no-subs", action="store_true")

    playlist_p = sub.add_parser("playlist", help="Download a full playlist")
    playlist_p.add_argument("url")
    playlist_p.add_argument("-o", "--output-dir", default=".")
    playlist_p.add_argument("-f", "--format", default="mp4", choices=["mp4", "mkv"])
    playlist_p.add_argument("-s", "--subs", nargs="*", default=["en"])
    playlist_p.add_argument("--no-auto-subs", action="store_true")

    args = parser.parse_args()

    if args.command == "video":
        download_video(
            video_url=args.url,
            output_dir=args.output_dir,
            output_format=args.format,
            max_resolution=args.resolution,
            subtitle_langs=None if args.no_subs else args.subs,
        )
    elif args.command == "playlist":
        download_playlist(
            playlist_url=args.url,
            output_format=args.format,
            subtitle_langs=args.subs,
            download_auto_subs=not args.no_auto_subs,
            output_dir=args.output_dir,
        )
