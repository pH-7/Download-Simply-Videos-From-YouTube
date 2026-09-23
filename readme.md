# 📥 Download Any Videos From YouTube

**⚡️ High-Quality YouTube Video, Playlist & Channel Downloader 🎥**

![Demo. Download any YouTube videos and YouTube playlists](promo-assets/demo-download-youtube-videos-script.gif)

> [!Note]
>
> #### 🚀 The Ultimate YouTube Downloader
> 
> Download single videos, entire playlists, complete channels, or multiple URLs simultaneously with intelligent concurrent processing and smart organization!

This powerful Python script downloads YouTube content in the highest available quality while handling multiple formats efficiently. Perfect for content creators, educators, and anyone who needs reliable YouTube downloads!

**✨ What makes this special?**
- 🎯 **Smart URL Detection** - Automatically detects videos, playlists, and channels
- ⚡ **Lightning-Fast Concurrent Downloads** - Download multiple videos/playlists/channels simultaneously
- 🗂️ **Intelligent Organization** - Playlists and channels get organized folders
- 📺 **Full Channel Support** - Download entire YouTube channels with date-organized files
- 🎵 **MP3 Audio Option** - Download high-quality audio only in MP3 format
- 🛡️ **Bulletproof Error Handling** - One failed download won't stop the others
- 🧠 **Intuitive UX** - Only shows relevant options when needed

- [⚙️ Requirements](#%EF%B8%8F-requirements)
- [📦 Installation](#-installation)
- [🪄 Usage](#-usage)
- [🎵 Playlist Downloads](#-playlist-downloads)
- [� Channel Downloads](#-channel-downloads)
- [�🛠️ Configuration](#%EF%B8%8F-configuration)
- [🧹 Clean Up Incomplete Downloads](#-optional-clean-up-incomplete-downloads)
- [👨‍🍳 Who is the creator?](#-who-created-this)
- [🤝 Contributing](#-contributing)
- [⚖️ License](#%EF%B8%8F-license)

## ⚙️ Requirements
* [Python v3.10](https://www.python.org/downloads/) or higher 🐍
* FFmpeg installed on your system 🎬
* YouTube URLs (videos, playlists, or channels) that you have permission to download 📝


## 📦 Installation

Open a terminal in the project folder, then follow these steps:

1. **Clone the repository**

   ```bash
   git clone https://github.com/pH-7/Download-Simply-Videos-From-YouTube.git
   cd Download-Simply-Videos-From-YouTube
   ```

2. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt # pip3 install -r requirements.txt
   ```

3. **Install FFmpeg**

   * **macOS**

     ```bash
     brew install ffmpeg
     ```
   * **Ubuntu/Debian**

     ```bash
     sudo apt-get install ffmpeg
     ```
   * **Windows**
     Download FFmpeg from the [official website](https://ffmpeg.org/download.html), follow the installation guide, and add it to your `PATH`.
   Download from the [FFmpeg website](https://ffmpeg.org/download.html), follow the instructions and add to PATH

## 🪄 Usage

### Basic Usage

To run the script, use the following command:

```console
python download.py # python3 download.py
```

### Single Video Download
Enter a single YouTube URL when prompted:
```
Enter YouTube URL(s): https://www.youtube.com/watch?v=Hhb8ghB8lMg
```

**For single videos, the script automatically optimizes the process by:**
- ✨ Skipping the concurrent downloads prompt (not needed for single videos)
- 🎯 Using streamlined single-threaded processing
- 📁 Direct file placement in your chosen directory

### Multiple Videos Download 🆕
You can download multiple videos simultaneously by entering URLs in various formats. The script intelligently parses different input methods:

#### **Method 1: Comma-Separated URLs**
```
Enter YouTube URL(s): https://www.youtube.com/watch?v=Hhb8ghB8lMg, https://www.youtube.com/watch?v=RiCUh_V7Tjg, https://www.youtube.com/watch?v=HcioaU54p08
```

#### **Method 2: Space-Separated URLs**
```
Enter YouTube URL(s): https://www.youtube.com/watch?v=Hhb8ghB8lMg https://www.youtube.com/watch?v=RiCUh_V7Tjg https://www.youtube.com/watch?v=HcioaU54p08
```

#### **Method 3: Mixed Format**
You can combine commas and spaces in any way:
```
Enter YouTube URL(s): https://www.youtube.com/watch?v=Hhb8ghB8lMg, https://www.youtube.com/watch?v=RiCUh_V7Tjg https://www.youtube.com/watch?v=HcioaU54p08, https://www.youtube.com/watch?v=ghi789
```

#### **Method 4: Multi-Line Input**
For easier management of many URLs, press **Enter** without typing anything when prompted, then enter one URL per line:

```
Enter YouTube URL(s): [Press Enter here]
📝 Multi-line mode activated!
💡 Enter one URL per line, press Enter twice when finished:
   URL 1: https://www.youtube.com/watch?v=Hhb8ghB8lMg
   URL 2: https://www.youtube.com/watch?v=RiCUh_V7Tjg
   URL 3: https://www.youtube.com/watch?v=HcioaU54p08
   URL 4: [Press Enter here to finish]
```

#### **Benefits of Multi-Video Download:**
- ⚡ **Concurrent processing**: Downloads happen simultaneously (configurable 1-5 workers)
- 🛡️ **Independent operations**: One failed download won't stop others
- 📊 **Progress tracking**: See individual download status and final summary
- 🎯 **Smart validation**: Invalid URLs are automatically skipped with warnings
- 🧠 **Intelligent prompting**: Concurrent options only appear when downloading multiple videos

### MP3 Audio Downloads 🎵
You can download audio-only versions of videos and playlists in high-quality MP3 format:

When prompted during download, choose:
```
Choose format:
  1. MP4 Video (default)
  2. MP3 Audio only
Enter choice (1-2, default=1): 2
```

**MP3 Features:**
- 🎵 **High Quality**: 192kbps MP3 extraction using FFmpeg
- 📁 **Smart Organization**: Works with playlists - creates MP3 files in playlist folders
- ⚡ **Fast Processing**: Optimized audio extraction
- 🎯 **Clean Output**: Pure MP3 files without video data

**Perfect for:**
- Music playlists
- Podcasts and interviews
- Educational content
- Language learning materials

## 🎵 Playlist Downloads
The script fully supports YouTube playlist downloads with smart organization and **concurrent playlist processing**!

### **Single Playlist**
```
Enter YouTube URL(s): https://www.youtube.com/playlist?list=PLxxxxxxx
```

### **Multiple Playlists Concurrently** 🚀
Download multiple playlists simultaneously using any input method:
```
Enter YouTube URL(s): https://www.youtube.com/playlist?list=PLxxxxxx, https://www.youtube.com/playlist?list=PLyyyyyy
```

### **Mixed Content Downloads** 🎯
Combine videos and playlists in one go:
```
Enter YouTube URL(s): https://www.youtube.com/watch?v=abc123, https://www.youtube.com/playlist?list=PLxxxxxx, https://www.youtube.com/watch?v=def456
```

**🌟 Playlist Features:**
- 🗂️ **Smart organization**: Each playlist creates its own folder named after the playlist title
- 🔢 **Numbered files**: Videos are numbered according to their playlist order
- ⚡ **Concurrent playlist downloads**: Multiple playlists download simultaneously
- 📊 **Progress tracking**: See individual playlist progress and video counts
- 🛡️ **Error resilience**: Failed videos in a playlist won't stop the entire playlist download

**📁 File Structure Example:**
```
downloads/
├── My Awesome Playlist/
│   ├── 01-First Video.mp4
│   ├── 02-Second Video.mp4
│   └── 03-Third Video.mp4
├── Another Great Playlist/
│   ├── 01-Another Video.mp4
│   └── 02-Last Video.mp4
└── Individual Video.mp4
```

## 📺 Channel Downloads
Download entire YouTube channels with all their uploaded videos! The script supports all YouTube channel URL formats and organizes videos by upload date.

### **Supported Channel URL Formats**
The script automatically detects and handles all YouTube channel URL formats:

```
Enter YouTube URL(s): https://www.youtube.com/@channelname
```

**All supported formats:**
- `https://www.youtube.com/@channelname` (New @handle format)
- `https://www.youtube.com/channel/UCxxxxxxxxx` (Channel ID format)
- `https://www.youtube.com/c/channelname` (Custom URL format)
- `https://www.youtube.com/user/username` (Legacy user format)

### **Channel Download Features**
- 📺 **Complete Channel Downloads** - Gets ALL videos from a channel
- 📅 **Date-Organized Files** - Videos organized by upload date (YYYYMMDD-Title)
- 📁 **Channel Folders** - Each channel gets its own folder named after the channel
- ⚡ **Concurrent Channel Downloads** - Download multiple channels simultaneously
- 🎵 **MP3 Support** - Full audio-only support for channels
- 🔄 **Progress Tracking** - See real-time download progress for large channels

### **Channel Examples**

#### **Single Channel**
```
Enter YouTube URL(s): https://www.youtube.com/@pH7Programming
```

#### **Multiple Channels Concurrently** 🚀
```
Enter YouTube URL(s): https://www.youtube.com/@TechChannel, https://www.youtube.com/@MusicChannel
```

#### **Mixed Content Downloads** 🎯
Combine channels, playlists, and individual videos:
```
Enter YouTube URL(s): https://www.youtube.com/@TechChannel, https://www.youtube.com/playlist?list=PLxxxxxx, https://www.youtube.com/watch?v=abc123
```

**📁 Channel File Structure Example:**
```
downloads/
├── TechChannel/
│   ├── 20240815-Latest Tech Review.mp4
│   ├── 20240810-Programming Tutorial.mp4
│   └── 20240805-Tech News Update.mp4
├── MusicChannel/
│   ├── 20240820-New Song Release.mp3
│   └── 20240815-Behind the Scenes.mp3
└── Individual Video.mp4
```

⚠️ **Channel Download Notes:**
- Large channels may take significant time to download
- Consider using MP3-only mode for music channels to save space
- The script respects YouTube's rate limits to avoid blocks
- Failed videos won't stop the entire channel download

### Advanced Options

#### List Available Formats
To see what video formats are available for a specific video:
```console
python download.py --list-formats
```

#### Concurrent Downloads (Multiple Videos Only)
When downloading multiple videos, the script will prompt you to choose concurrent workers (1-5, default: 3):
```
Number of concurrent downloads (1-5, default=3): 5
```

**Note:** This prompt only appears when downloading multiple videos. Single video downloads are automatically optimized for best performance.

**The script will:**
1. Prompt for YouTube URL(s) (single video, playlist, or multiple URLs)
2. Ask for an output directory (optional)
3. **Smart prompting**: Ask for concurrent downloads only when downloading multiple videos
4. Download content simultaneously in the highest available quality (for multiple videos)
5. Organize content appropriately:
   - Single videos: Saved directly in the output directory
   - Playlists: Organized in a playlist-named folder with numbered files
   - Multiple videos: All saved to the same output directory
6. Provide a detailed summary of successful and failed downloads

**🌟 Key Features:**
- ✨ Support for single videos, playlists, and **multiple URLs simultaneously** (including multiple playlists)
- 🎥 High-quality video and audio downloads (up to 1080p)
- 🎵 **MP3 audio-only downloads** with high-quality 192kbps extraction
- 📁 Organized folder structure with smart playlist handling
- ⚡ **Unlimited concurrent downloading** for videos and playlists - ideal for super-fast batch downloads
- 🔄 Format conversion to MP4 or MP3
- 🛡️ Error handling and recovery with detailed reporting
- 📊 Download progress tracking and summary reports
- 🎯 Smart URL parsing and validation
- 🧠 **Intelligent UX**: Relevant prompts only when applicable

### Usage Examples

**Download single video:**
```bash
python download.py
# Enter: https://www.youtube.com/watch?v=Hhb8ghB8lMg
# Note: No concurrent downloads prompt - automatically optimized!
```

**Download multiple videos (comma-separated):**
```bash
python download.py
# Enter: https://www.youtube.com/watch?v=Hhb8ghB8lMg, https://www.youtube.com/watch?v=RiCUh_V7Tjg
# Concurrent downloads prompt will appear
```

**Download multiple playlists simultaneously:**
```bash
python download.py
# Enter: https://www.youtube.com/playlist?list=PLxxxxxx, https://www.youtube.com/playlist?list=PLyyyyyy
# Each playlist will be downloaded concurrently in its own organized folder!
```

**Download mixed content (videos + playlists):**
```bash
python download.py
# Enter: video_url1, playlist_url1, video_url2, playlist_url2
# Smart organization: Videos go to main folder, playlists get their own folders
```

**Download multiple videos (space-separated):**
```bash
python download.py
# Enter: https://www.youtube.com/watch?v=Hhb8ghB8lMg https://www.youtube.com/watch?v=RiCUh_V7Tjg
# Concurrent downloads prompt will appear
```

**Download multiple videos (mixed format):**
```bash
python download.py
# Enter: url1, url2 url3, url4 url5
# Concurrent downloads prompt will appear
```

**Download multiple videos (multi-line):**
```bash
python download.py
# Press Enter when prompted, then:
# URL 1: https://www.youtube.com/watch?v=Hhb8ghB8lMg
# URL 2: https://www.youtube.com/watch?v=RiCUh_V7Tjg
# URL 3: [Press Enter to finish]
# Concurrent downloads prompt will appear
```

**Download with custom concurrent settings:**
```bash
python download.py
# Enter multiple URLs using any method above
# Choose output directory: /Users/john/Videos
# Choose concurrent downloads: 5 (only for multiple videos)
```

**Debug format issues:**
```bash
python download.py --list-formats
# Enter problematic URL to see available formats
```

## 🛠️ Configuration

You can modify the following in the script:
- Video format preferences (currently limited to 1080p max)
- Maximum concurrent downloads (1-5 workers, automatically applied only for multiple videos)
- Output directory structure
- Post-processing options
- Retry attempts for failed downloads

## 🧹 Optional: Clean Up Incomplete Downloads

If you ever experience interrupted downloads (e.g., due to network issues or stopping the script), you may find leftover `.part` or `.ytdl` files in your `downloads/` folder. These are incomplete files and can be safely removed.

A utility script, `cleanup_downloads.py`, is included to help you quickly clean up these incomplete files:

```bash
python cleanup_downloads.py
```

This will scan your `downloads/` directory and remove any partial or temporary files, leaving only your completed videos and audio files. Most users will not need this, but it's handy for keeping your downloads folder tidy after interruptions.

## 👨‍🍳 Who cooked this?

[![Pierre-Henry Soria](https://s.gravatar.com/avatar/a210fe61253c43c869d71eaed0e90149?s=200)](https://PH7.me 'Pierre-Henry Soria personal website')

**Pierre-Henry Soria**. A passionate **software AI engineer** who loves automating content creation! 🚀 Enthusiast for YouTube, photography, AI, learning, and health! 😊 Find me at [pH7.me](https://ph7.me) 🚀

☕️ Do you enjoy this project? **[Offer me a coffee](https://ko-fi.com/phenry)** (spoiler alert: I love almond flat white! 😋)

[![@phenrysay][x-icon]](https://x.com/phenrysay "Follow Me on X") [![pH-7][github-icon]](https://github.com/pH-7 "Follow Me on GitHub") [![YouTube Tech Videos][youtube-icon]](https://www.youtube.com/@pH7Programming "My YouTube Tech Channel") [![BlueSky][bsky-icon]](https://bsky.app/profile/ph7.me "Follow Me on BlueSky")

## 🤝 Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## ⚖️ License

**Download Simply Videos From YouTube** is generously distributed under the *[MIT License](https://opensource.org/licenses/MIT)* 🎉 Enjoy!

## ⚠️ Disclaimer

This script is for educational purposes only. Before using this script, please **ensure you have the right to download the content and that you comply with YouTube's terms of service**.

<!-- GitHub's Markdown reference links -->
[x-icon]: https://img.shields.io/badge/x-000000?style=for-the-badge&logo=x
[bsky-icon]: https://img.shields.io/badge/BlueSky-00A8E8?style=for-the-badge&logo=bluesky&logoColor=white
[github-icon]: https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white
[youtube-icon]: https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white
