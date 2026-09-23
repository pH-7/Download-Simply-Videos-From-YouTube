from yt_dlp import YoutubeDL
import os
from typing import Optional

def download_playlist(playlist_url: str, output_path: Optional[str] = None) -> None:
    """
    Download a YouTube playlist in high quality.
    
    Args:
        playlist_url (str): URL of the YouTube playlist
        output_path (str, optional): Directory to save the downloads. Defaults to './downloads'
    """
    # Set default output path if none provided
    if output_path is None:
        output_path = os.path.join(os.getcwd(), 'downloads')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Prefer high quality MP4
        'outtmpl': os.path.join(output_path, '%(playlist_title)s', '%(playlist_index)s-%(title)s.%(ext)s'),
        'ignoreerrors': True,  # Skip unavailable videos
        'nocheckcertificate': True,
        'geo_bypass': True,
        'quiet': False,
        'no_warnings': False,
        'extract_flat': False,
        'writethumbnail': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],  # Download English subtitles if available
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Download playlist
            ydl.download([playlist_url])
            print(f"\nDownload completed successfully! Files saved to: {output_path}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Example usage
    playlist_url = input("Enter the YouTube playlist URL: ")
    output_dir = input("Enter output directory (press Enter for default): ").strip()
    
    if output_dir:
        download_playlist(playlist_url, output_dir)
    else:
        download_playlist(playlist_url)