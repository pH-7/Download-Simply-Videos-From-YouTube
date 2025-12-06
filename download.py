import sys
from yt_dlp import YoutubeDL
import os
import re
import time
from typing import Optional, List, Dict, Tuple
from urllib.parse import urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache

MAX_RETRIES = 3
RETRY_DELAY = 2
MAX_CONCURRENT_WORKERS = 5
DEFAULT_CONCURRENT_WORKERS = 3


@lru_cache(maxsize=128)
def get_url_info(url: str) -> Tuple[str, Dict]:
    """
    Get URL information with caching to avoid duplicate yt-dlp calls.
    Returns (content_type, info_dict) for efficient reuse.

    Args:
        url (str): YouTube URL to analyze

    Returns:
        Tuple[str, Dict]: (content_type, info_dict) where content_type is 'video', 'playlist', or 'channel'
    """
    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'no_warnings': True,
            'skip_download': True,
            'playlist_items': '1',
        }

        with YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(url, download=False)

            if video_info is None:
                parsed_url = urlparse(url)
                query_params = parse_qs(parsed_url.query)
                if '/@' in url or '/channel/' in url or '/c/' in url or '/user/' in url:
                    return 'channel', {}
                elif 'list' in query_params:
                    return 'playlist', {}
                else:
                    return 'video', {}

            content_type = video_info.get('_type', 'video')

            if content_type == 'playlist':
                if video_info.get('uploader_id') and ('/@' in url or '/channel/' in url or '/c/' in url or '/user/' in url):
                    return 'channel', video_info
                else:
                    return 'playlist', video_info

            return content_type, video_info

    except Exception:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        if '/@' in url or '/channel/' in url or '/c/' in url or '/user/' in url:
            return 'channel', {}
        elif 'list' in query_params:
            return 'playlist', {}
        else:
            return 'video', {}


def get_content_type(url: str) -> str:
    """
    Get the content type of a YouTube URL.

    Args:
        url (str): YouTube URL to analyze

    Returns:
        str: 'video', 'playlist', or 'channel'
    """
    content_type, _ = get_url_info(url)
    return content_type


def parse_multiple_urls(input_string: str) -> List[str]:
    """
    Parse multiple URLs from input string separated by commas, spaces, newlines, or mixed formats.
    Handles complex mixed separators like "url1, url2 url3\nurl4".

    Args:
        input_string (str): String containing one or more URLs

    Returns:
        List[str]: List of cleaned URLs
    """
    urls = re.split(r'[,\s\n\t]+', input_string.strip())
    urls = [url.strip() for url in urls if url.strip()]

    valid_urls = []
    invalid_count = 0
    for url in urls:
        if ('youtube.com' in url or 'youtu.be' in url) and (
            '/watch?' in url or
            '/playlist?' in url or
            '/@' in url or
            '/channel/' in url or
            '/c/' in url or
            '/user/' in url or
            'youtu.be/' in url
        ):
            valid_urls.append(url)
        elif url:
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
    except Exception as error:
        print(f"Error listing formats: {str(error)}")


def download_single_video(url: str, output_path: str, thread_id: int = 0, audio_only: bool = False) -> dict:
    """
    Download a single YouTube video, playlist, or channel with retry mechanism.

    Args:
        url (str): YouTube URL to download (video, playlist, or channel)
        output_path (str): Directory to save the download
        thread_id (int): Thread identifier for logging
        audio_only (bool): If True, download audio only in MP3 format

    Returns:
        dict: Result status with success/failure info
    """
    if audio_only:
        format_selector = 'bestaudio/best'
        file_extension = 'mp3'
        postprocessors = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        print(f"🎵 [Thread {thread_id}] Audio-only mode: Downloading MP3...")
    else:
        format_selector = (
            'bestvideo[height<=1080]+bestaudio/best[height<=1080]/'
            'best'
        )
        file_extension = 'mp4'
        postprocessors = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]

    downloader_options = {
        'format': format_selector,
        'ignoreerrors': True,
        'no_warnings': False,
        'extract_flat': False,
        'writesubtitles': False,
        'writethumbnail': False,
        'writeautomaticsub': False,
        'postprocessors': postprocessors,
        'keepvideo': False,
        'clean_infojson': True,
        'retries': MAX_RETRIES,
        'fragment_retries': MAX_RETRIES,
        'noplaylist': False,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios', 'web'],
                'player_skip': ['webpage', 'configs'],
            }
        },
        'nocheckcertificate': True,
        'age_limit': None,
        'http_headers': {
            'User-Agent': 'com.google.android.youtube/17.36.4 (Linux; U; Android 12; GB) gzip',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Sec-Fetch-Mode': 'navigate',
        },
    }

    if not audio_only:
        downloader_options['merge_output_format'] = 'mp4'

    content_type, _ = get_url_info(url)

    if content_type == 'playlist':
        downloader_options['outtmpl'] = os.path.join(
            output_path, '%(playlist_title)s', f'%(playlist_index)s-%(title)s.{file_extension}')
        print(f"📋 [Thread {thread_id}] Detected playlist URL. Downloading entire playlist...")
        print(f"📁 [Thread {thread_id}] Files will be saved to: {output_path}/[playlist_name]/")
    elif content_type == 'channel':
        downloader_options['outtmpl'] = os.path.join(
            output_path, '%(uploader)s', f'%(upload_date)s-%(title)s.{file_extension}')
        print(f"📺 [Thread {thread_id}] Detected channel URL. Downloading entire channel...")
        print(f"📁 [Thread {thread_id}] Files will be saved to: {output_path}/[channel_name]/")
    else:
        downloader_options['outtmpl'] = os.path.join(
            output_path, f'%(title)s.{file_extension}')
        print(f"🎥 [Thread {thread_id}] Detected single video URL. Downloading {'audio' if audio_only else 'video'}...")
        print(f"📁 [Thread {thread_id}] File will be saved to: {output_path}/")

    last_exception = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with YoutubeDL(downloader_options) as ydl:
                download_result = ydl.extract_info(url, download=True)

                if download_result is None:
                    return {
                        'url': url,
                        'success': False,
                        'message': f"❌ [Thread {thread_id}] Failed to extract video information. Video may be private or unavailable."
                    }

                if download_result.get('_type') == 'playlist':
                    title = download_result.get('title', 'Unknown Playlist')
                    video_count = len(download_result.get('entries', []))
                    print(f"📋 [Thread {thread_id}] {content_type.title()}: '{title}' ({video_count} videos)")

                    if video_count == 0:
                        return {
                            'url': url,
                            'success': False,
                            'message': f"❌ [Thread {thread_id}] {content_type.title()} appears to be empty or private"
                        }

                    return {
                        'url': url,
                        'success': True,
                        'message': f"✅ [Thread {thread_id}] {content_type.title()} '{title}' download completed! ({video_count} {'MP3s' if audio_only else 'videos'}) 📂 Location: {output_path}"
                    }
                else:
                    title = download_result.get('title', 'Unknown')
                    return {
                        'url': url,
                        'success': True,
                        'message': f"✅ [Thread {thread_id}] {'Audio' if audio_only else 'Video'} '{title}' download completed! 📂 Location: {output_path}"
                    }

        except Exception as error:
            last_exception = error
            if attempt < MAX_RETRIES:
                retry_delay = RETRY_DELAY * (2 ** (attempt - 1))
                error_msg = f"⚠️  [Thread {thread_id}] Attempt {attempt}/{MAX_RETRIES} failed: {str(error)[:100]}. Retrying in {retry_delay}s..."
                print(error_msg)
                time.sleep(retry_delay)
            else:
                return {
                    'url': url,
                    'success': False,
                    'message': f"❌ [Thread {thread_id}] Failed after {MAX_RETRIES} attempts. Last error: {str(last_exception)}"
                }

    return {
        'url': url,
        'success': False,
        'message': f"❌ [Thread {thread_id}] Unexpected error: {str(last_exception)}"
    }


def download_youtube_content(urls: List[str], output_path: Optional[str] = None,
                             list_formats: bool = False, max_workers: int = DEFAULT_CONCURRENT_WORKERS, 
                             audio_only: bool = False) -> None:
    """
    Download YouTube content (single videos, playlists, or channels) in MP4 format or MP3 audio only.
    Supports multiple URLs for simultaneous downloading with optimized concurrency.

    Args:
        urls (List[str]): List of YouTube URLs to download (videos, playlists, or channels)
        output_path (str, optional): Directory to save the downloads. Defaults to './downloads'
        list_formats (bool): If True, only list available formats without downloading
        max_workers (int): Maximum number of concurrent downloads (1-5, default=3)
        audio_only (bool): If True, download audio only in MP3 format
    """
    if output_path is None:
        output_path = os.path.join(os.getcwd(), 'downloads')

    if list_formats:
        print("Available formats for the first provided URL:")
        get_available_formats(urls[0])
        return

    os.makedirs(output_path, exist_ok=True)

    print(
        f"\n🚀 Starting download of {len(urls)} URL(s) with {max_workers} concurrent workers...")
    print(f"📁 Output directory: {output_path}")
    print(f"🎧 Format: {'MP3 Audio Only' if audio_only else 'MP4 Video'}")

    playlist_count = sum(
        1 for url in urls if get_content_type(url) == 'playlist')
    channel_count = sum(
        1 for url in urls if get_content_type(url) == 'channel')
    video_count = len(urls) - playlist_count - channel_count

    content_summary = []
    if playlist_count > 0:
        content_summary.append(f"{playlist_count} playlist(s)")
    if channel_count > 0:
        content_summary.append(f"{channel_count} channel(s)")
    if video_count > 0:
        content_summary.append(f"{video_count} video(s)")

    if content_summary:
        print(f"📋 Content: {' + '.join(content_summary)}")
    else:
        print("🎥 Content: Unknown content type")

    print("-" * 60)

    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(download_single_video, url, output_path, i+1, audio_only): url
            for i, url in enumerate(urls)
        }

        for future in as_completed(future_to_url):
            result = future.result()
            results.append(result)
            print(result['message'])

    print("\n" + "=" * 60)
    print("📊 DOWNLOAD SUMMARY")
    print("=" * 60)

    successful_downloads = [r for r in results if r['success']]
    failed_downloads = [r for r in results if not r['success']]

    print(f"✅ Successful downloads: {len(successful_downloads)}")
    print(f"❌ Failed downloads: {len(failed_downloads)}")

    if failed_downloads:
        print("\n❌ Failed URLs:")
        for result in failed:
            print(f"   • {result['url']}")
            print(f"     Reason: {result['message']}")

    if successful:
        print(f"\n🎉 All files saved to: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--list-formats':
        url = input("Enter the YouTube URL to list formats: ")
        download_youtube_content([url], list_formats=True)
    else:
        print("📥 YouTube Multi-Content Downloader")
        print("=" * 50)
        print("💡 SUPPORTED INPUT FORMATS:")
        print("   🔸 Single URL: Just paste one YouTube URL")
        print("   🔸 Comma-separated: url1, url2, url3")
        print("   🔸 Space-separated: url1 url2 url3")
        print("   🔸 Mixed format: url1, url2 url3, url4")
        print("   🔸 Multi-line: Press Enter without typing, then one URL per line")
        print()
        print("🎯 SUPPORTED CONTENT TYPES:")
        print("   📹 Single Videos: https://www.youtube.com/watch?v=...")
        print("   📋 Playlists: https://www.youtube.com/playlist?list=...")
        print("   📺 Channels: https://www.youtube.com/@channelname")
        print("   📺 Channels: https://www.youtube.com/channel/UC...")
        print("   📺 Channels: https://www.youtube.com/c/channelname")
        print("   📺 Channels: https://www.youtube.com/user/username")
        print("-" * 50)

        user_input = input("Enter YouTube URL(s): ")

        if not user_input.strip():
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
            user_input = '\n'.join(urls_list)

        if not user_input.strip():
            print("❌ No URLs entered. Exiting...")
            exit(1)

        urls = parse_multiple_urls(user_input)

        if not urls:
            print("❌ No valid YouTube URLs found. Please try again.")
            exit(1)

        print(f"\n✅ Found {len(urls)} valid URL(s)")
        for i, url in enumerate(urls, 1):
            print(f"   {i}. {url}")

        output_dir = input(
            "\nEnter output directory (press Enter for default): "
        ).strip()

        format_choice = input(
            "\nChoose format:\n"
            "  1. MP4 Video (default)\n"
            "  2. MP3 Audio only\n"
            "Enter choice (1-2, default=1): ").strip()

        audio_only = False
        if format_choice == '2':
            audio_only = True
            print("🎵 Selected: MP3 Audio only")
        else:
            print("🎥 Selected: MP4 Video")

        max_workers = 1
        if len(urls) > 1:
            workers_input = input(
                f"Number of concurrent downloads (1-{MAX_CONCURRENT_WORKERS}, default={DEFAULT_CONCURRENT_WORKERS}): ").strip()
            try:
                max_workers = int(workers_input) if workers_input else DEFAULT_CONCURRENT_WORKERS
                max_workers = max(1, min(MAX_CONCURRENT_WORKERS, max_workers))
            except ValueError:
                max_workers = DEFAULT_CONCURRENT_WORKERS

        print(f"\n🎬 Starting downloads...")
        print(f"📊 URLs to download: {len(urls)}")
        print(f"🎧 Format: {'MP3 Audio' if audio_only else 'MP4 Video'}")
        if len(urls) > 1:
            print(f"⚡ Concurrent workers: {max_workers}")
        print(
            f"📁 Output: {output_dir if output_dir else 'default (./downloads)'}")

        if output_dir:
            download_youtube_content(
                urls, output_dir, max_workers=max_workers, audio_only=audio_only)
        else:
            download_youtube_content(
                urls, max_workers=max_workers, audio_only=audio_only)
