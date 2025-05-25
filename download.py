from yt_dlp import YoutubeDL
import os
from typing import Optional
from urllib.parse import urlparse, parse_qs


def is_playlist_url(url: str) -> bool:
    """
    Check if the provided URL is a playlist or a single video.

    Args:
        url (str): YouTube URL to check

    Returns:
        bool: True if URL is a playlist, False if single video
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return 'list' in query_params


def get_available_formats(url: str) -> None:
    """
    List available formats for debugging purposes.

    Args:
        url (str): YouTube URL to check formats for
    """
    ydl_opts = {
        'listformats': True,
        'quiet': False
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=False)
    except Exception as e:
        print(f"Error listing formats: {str(e)}")


def download_youtube_content(url: str, output_path: Optional[str] = None, list_formats: bool = False) -> None:
    """
    Download YouTube content (single video or playlist) in MP4 format only.

    Args:
        url (str): URL of the YouTube video or playlist
        output_path (str, optional): Directory to save the downloads. Defaults to './downloads'
        list_formats (bool): If True, only list available formats without downloading
    """
    # Set default output path if none provided
    if output_path is None:
        output_path = os.path.join(os.getcwd(), 'downloads')

    # If user wants to list formats, do that and return
    if list_formats:
        print("Available formats for the provided URL:")
        get_available_formats(url)
        return

    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    format_selector = (
        # Try best video+audio combination first
        'bestvideo[height<=1080]+bestaudio/best[height<=1080]/'
        # Fallback to best available quality
        'best'
    )

    # Configure yt-dlp options for MP4 only
    ydl_opts = {
        'format': format_selector,
        'merge_output_format': 'mp4',
        'ignoreerrors': True,
        'no_warnings': False,
        'extract_flat': False,
        # Disable all additional downloads for clean MP4-only output
        'writesubtitles': False,
        'writethumbnail': False,
        'writeautomaticsub': False,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        # Clean up options
        'keepvideo': False,
        'clean_infojson': True,
        'retries': 3,
        'fragment_retries': 3,
    }

    # Set different output templates for playlists and single videos
    if is_playlist_url(url):
        ydl_opts['outtmpl'] = os.path.join(
            output_path, '%(playlist_title)s', '%(playlist_index)s-%(title)s.%(ext)s')
        print("Detected playlist URL. Downloading entire playlist...")
    else:
        ydl_opts['outtmpl'] = os.path.join(output_path, '%(title)s.%(ext)s')
        print("Detected single video URL. Downloading video...")

    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Download content
            ydl.download([url])
            print(
                f"\nDownload completed successfully! Files saved to: {output_path}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("\nTroubleshooting suggestions:")
        print("1. Try running with --list-formats to see available formats:")
        print("   python download.py --list-formats")
        print("2. Check if the video is available in your region")
        print("3. Ensure you have the latest version of yt-dlp:")
        print("   pip install --upgrade yt-dlp")


if __name__ == "__main__":
    import sys

    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--list-formats':
        url = input("Enter the YouTube URL to list formats: ")
        download_youtube_content(url, list_formats=True)
    else:
        # Normal download flow
        url = input("Enter the YouTube URL (video or playlist): ")
        output_dir = input(
            "Enter output directory (press Enter for default): ").strip()

        print(f"\nStarting download...")
        print(f"URL: {url}")
        print(
            f"Output: {output_dir if output_dir else 'default (./downloads)'}")

        if output_dir:
            download_youtube_content(url, output_dir)
        else:
            download_youtube_content(url)
