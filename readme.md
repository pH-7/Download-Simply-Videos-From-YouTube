# 📥 Download Any Videos From YouTube

**⚡️ High-Quality YouTube Video & Playlist Downloader 🎥**

![Demo. Download any YouTube videos and YouTube playlists](promo-assets/demo-download-youtube-videos-script.gif)

> 🚀 **The Ultimate YouTube Downloader** - Download single videos, entire playlists, or multiple URLs simultaneously with intelligent concurrent processing and smart organization!

This powerful Python script downloads YouTube content in the highest available quality while handling multiple formats efficiently. Perfect for content creators, educators, and anyone who needs reliable YouTube downloads!

**✨ What makes this special?**
- 🎯 **Smart URL Detection** - Automatically detects single videos vs playlists
- ⚡ **Lightning-Fast Concurrent Downloads** - Download multiple videos/playlists simultaneously
- 🗂️ **Intelligent Organization** - Playlists get their own folders with numbered files
- 🛡️ **Bulletproof Error Handling** - One failed download won't stop the others
- 🧠 **Intuitive UX** - Only shows relevant options when needed

- [⚙️ Requirements](#%EF%B8%8F-requirements)
- [📦 Installation](#-installation)
- [🪄 Usage](#-usage)
- [🎵 Playlist Downloads](#-playlist-downloads)
- [🛠️ Configuration](#%EF%B8%8F-configuration)
- [👨‍🍳 Who is the creator?](#-who-created-this)
- [🤝 Contributing](#-contributing)
- [⚖️ License](#%EF%B8%8F-license)

## ⚙️ Requirements
* [Python v3.7](https://www.python.org/downloads/) or higher 🐍
* FFmpeg installed on your system 🎬
* YouTube URLs (single videos or playlists) that you have permission to download 📝

## 📦 Installation

1. Clone this repository:
   ```console
   git clone https://github.com/pH-7/Download-Simply-Videos-From-YouTube.git && cd Download-Simply-Videos-From-YouTube
   ```

2. Install the required Python packages:
   ```console
   pip install -r requirements.txt
   ```

3. Install FFmpeg:
   - **macOS:**
     ```console
     brew install ffmpeg
     ```
   - **Ubuntu/Debian:**
     ```console
     sudo apt-get install ffmpeg
     ```
   - **Windows:**
      Download from the [FFmpeg website](https://ffmpeg.org/download.html), follow the instructions and add to PATH

## 🪄 Usage

### Basic Usage

To run the script, use the following command:

```console
python download.py
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
- 📁 Organized folder structure with smart playlist handling
- ⚡ **Unlimited concurrent downloading** for videos and playlists - ideal for super-fast batch downloads
- 🔄 Format conversion to MP4
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

## 👨‍🍳 Who cooked this?

[![Pierre-Henry Soria](https://s.gravatar.com/avatar/a210fe61253c43c869d71eaed0e90149?s=200)](https://PH7.me 'Pierre-Henry Soria personal website')

**Pierre-Henry Soria**. A passionate **software AI engineer** who loves automating content creation! 🚀 Enthusiast for YouTube, photography, AI, learning, and health! 😊 Find me at [pH7.me](https://ph7.me) 🚀

☕️ Do you enjoy this project? **[Offer me a coffee](https://ko-fi.com/phenry)** (spoiler alert: I love almond flat white! 😋)

[![@phenrysay][x-icon]](https://x.com/phenrysay "Follow Me on X") [![pH-7][github-icon]](https://github.com/pH-7 "Follow Me on GitHub") [![YouTube Tech Videos][youtube-icon]](https://www.youtube.com/@pH7Programming "My YouTube Tech Channel")

## 🤝 Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## ⚖️ License

**Download Simply Videos From YouTube** is generously distributed under the *[MIT License](https://opensource.org/licenses/MIT)* 🎉 Enjoy!

## ⚠️ Disclaimer

This script is for educational purposes only. Please ensure you have the right to download any content and comply with YouTube's terms of service when using this script.

<!-- GitHub's Markdown reference links -->
[x-icon]: https://img.shields.io/badge/x-000000?style=for-the-badge&logo=x
[github-icon]: https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white
[youtube-icon]: https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white
