from yt_dlp import YoutubeDL
import os
import re
from typing import Optional, List
from urllib.parse import urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


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


def parse_multiple_urls(input_string: str) -> List[str]:
    """
    Parse multiple URLs from input string separated by commas, spaces, newlines, or mixed formats.
    Handles complex mixed separators like "url1, url2 url3\nurl4".

    Args:
        input_string (str): String containing one or more URLs

    Returns:
        List[str]: List of cleaned URLs
    """
    # Use regex to split by multiple separators: comma, space, newline, tab
    urls = re.split(r'[,\s\n\t]+', input_string.strip())
    urls = [url.strip() for url in urls if url.strip()]

    # Validate URLs (basic YouTube URL check)
    valid_urls = []
    invalid_count = 0
    for url in urls:
        if 'youtube.com' in url or 'youtu.be' in url:
            valid_urls.append(url)
        elif url:  # Only show warning for non-empty strings
            print(f"⚠️  Skipping invalid URL: {url}")
            invalid_count += 1

    if invalid_count > 0:
        print(
            f"💡 Found {len(valid_urls)} valid YouTube URLs, skipped {invalid_count} invalid entries")

    return valid_urls


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


def download_single_video(url: str, output_path: str, thread_id: int = 0) -> dict:
    """
    Download a single YouTube video or playlist.

    Args:
        url (str): YouTube URL to download
        output_path (str): Directory to save the download
        thread_id (int): Thread identifier for logging

    Returns:
        dict: Result status with success/failure info
    """
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
        print(
            f"🎵 [Thread {thread_id}] Detected playlist URL. Downloading entire playlist...")
    else:
        ydl_opts['outtmpl'] = os.path.join(output_path, '%(title)s.%(ext)s')
        print(
            f"🎥 [Thread {thread_id}] Detected single video URL. Downloading video...")

    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Download content
            ydl.download([url])
            return {
                'url': url,
                'success': True,
                'message': f"✅ [Thread {thread_id}] Download completed successfully!"
            }

    except Exception as e:
        return {
            'url': url,
            'success': False,
            'message': f"❌ [Thread {thread_id}] Error: {str(e)}"
        }


def download_youtube_content(urls: List[str], output_path: Optional[str] = None,
                             list_formats: bool = False, max_workers: int = 3) -> None:
    """
    Download YouTube content (single videos or playlists) in MP4 format only.
    Supports multiple URLs for simultaneous downloading.

    Args:
        urls (List[str]): List of YouTube URLs to download
        output_path (str, optional): Directory to save the downloads. Defaults to './downloads'
        list_formats (bool): If True, only list available formats without downloading
        max_workers (int): Maximum number of concurrent downloads
    """
    # Set default output path if none provided
    if output_path is None:
        output_path = os.path.join(os.getcwd(), 'downloads')

    # If user wants to list formats, do that for the first URL and return
    if list_formats:
        print("Available formats for the first provided URL:")
        get_available_formats(urls[0])
        return

    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    print(
        f"\n🚀 Starting download of {len(urls)} URL(s) with {max_workers} concurrent workers...")
    print(f"📁 Output directory: {output_path}")
    print("-" * 60)

    # Download videos concurrently
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all download tasks
        future_to_url = {
            executor.submit(download_single_video, url, output_path, i+1): url
            for i, url in enumerate(urls)
        }

        # Collect results as they complete
        for future in as_completed(future_to_url):
            result = future.result()
            results.append(result)
            print(result['message'])

    # Print summary
    print("\n" + "=" * 60)
    print("📊 DOWNLOAD SUMMARY")
    print("=" * 60)

    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]

    print(f"✅ Successful downloads: {len(successful)}")
    print(f"❌ Failed downloads: {len(failed)}")

    if failed:
        print("\n❌ Failed URLs:")
        for result in failed:
            print(f"   • {result['url']}")
            print(f"     Reason: {result['message']}")

    if successful:
        print(f"\n🎉 All files saved to: {output_path}")


if __name__ == "__main__":
    import sys

    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--list-formats':
        url = input("Enter the YouTube URL to list formats: ")
        download_youtube_content([url], list_formats=True)
    else:
        # Normal download flow
        print("📥 YouTube Multi-Video Downloader")
        print("=" * 50)
        print("💡 SUPPORTED INPUT FORMATS:")
        print("   🔸 Single URL: Just paste one YouTube URL")
        print("   🔸 Comma-separated: url1, url2, url3")
        print("   🔸 Space-separated: url1 url2 url3")
        print("   🔸 Mixed format: url1, url2 url3, url4")
        print("   🔸 Multi-line: Press Enter without typing, then one URL per line")
        print("-" * 50)

        urls_input = input("Enter YouTube URL(s): ")

        # Handle multi-line input
        if not urls_input.strip():
            print("📝 Multi-line mode activated!")
            print("💡 Enter one URL per line, press Enter twice when finished:")
            urls_list = []
            line_count = 1
            while True:
                line = input(f"   URL {line_count}: ")
                if line.strip() == "":
                    break
                urls_list.append(line)
                line_count += 1
            urls_input = '\n'.join(urls_list)

        if not urls_input.strip():
            print("❌ No URLs entered. Exiting...")
            exit(1)

        urls = parse_multiple_urls(urls_input)

        if not urls:
            print("❌ No valid YouTube URLs found. Please try again.")
            exit(1)

        print(f"\n✅ Found {len(urls)} valid URL(s)")
        for i, url in enumerate(urls, 1):
            print(f"   {i}. {url}")

        output_dir = input(
            "\nEnter output directory (press Enter for default): ").strip()

        # Ask for concurrent workers (optional)
        workers_input = input(
            "Number of concurrent downloads (1-5, default=3): ").strip()
        try:
            max_workers = int(workers_input) if workers_input else 3
            max_workers = max(1, min(5, max_workers))  # Clamp between 1-5
        except ValueError:
            max_workers = 3

        print(f"\n🎬 Starting downloads...")
        print(f"📊 URLs to download: {len(urls)}")
        print(f"⚡ Concurrent workers: {max_workers}")
        print(
            f"📁 Output: {output_dir if output_dir else 'default (./downloads)'}")

        if output_dir:
            download_youtube_content(urls, output_dir, max_workers=max_workers)
        else:
            download_youtube_content(urls, max_workers=max_workers)
