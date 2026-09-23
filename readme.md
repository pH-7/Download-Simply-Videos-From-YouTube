# 📥 Download Any Videos From YouTube

**High-Quality YouTube Video & Playlist Downloader 🎥**

![Demo. Download any YouTube videos and YouTube playlists](promo-assets/demo-download-youtube-videos-script.gif)

This python script not only downloads YouTube content in the highest available quality but also handles multiple formats, subtitles, and thumbnails efficiently. Perfect for content creators and educational purposes! 

- [⚙️ Requirements](#%EF%B8%8F-requirements)
- [📦 Installation](#-installation)
- [🪄 Usage](#-usage)
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
   - **Ubuntu/Debian:**
     ```console
     sudo apt-get install ffmpeg
     ```
   - **macOS:**
     ```console
     brew install ffmpeg
     ```
   - **Windows:**
      Download from the [FFmpeg website](https://ffmpeg.org/download.html), follow the instructions and add to PATH

## 🪄 Usage

To run the script, use the following command:

```console
python download.py
```

**The script will:**
1. Prompt for the YouTube URL (video or playlist)
2. Ask for an output directory (optional)
3. Download content in the highest available quality
4. Save thumbnails and subtitles
5. Organize content appropriately:
   - Single videos: Saved directly in the output directory
   - Playlists: Organized in a playlist-named folder with numbered files

**Features:**
- ✨ Support for both single videos and playlists
- 🎥 High-quality video and audio downloads
- 📁 Organized folder structure
- 📑 Automatic subtitle downloading
- 🖼️ Thumbnail extraction
- 🔄 Format conversion to MP4
- ⚡ Error handling and recovery

## 🛠️ Configuration

You can modify the following in the script:
- Video format preferences
- Subtitle language selection
- Output directory structure
- Post-processing options

## 👨‍🍳 Who cooked this?

[![Pierre-Henry Soria](https://s.gravatar.com/avatar/a210fe61253c43c869d71eaed0e90149?s=200)](https://PH7.me 'Pierre-Henry Soria personal website')

**Pierre-Henry Soria**. A passionate **software AI engineer** who loves automating content creation! 🚀 Enthusiast for YouTube, photography, AI, learning, and health! 😊 Find me at [pH7.me](https://ph7.me) 🚀

☕️ D you enjoy this project? **[Offer me a coffee](https://ko-fi.com/phenry)** (spoiler alert: I love almond flat white! 😋)

[![@phenrysay][twitter-icon]](https://x.com/phenrysay) [![pH-7][github-icon]](https://github.com/pH-7) [![YouTube Tech Videos][youtube-icon]](https://www.youtube.com/@pH7Programming "My YouTube Tech Channel")

## 🤝 Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## ⚖️ License

**Download Simply Videos From YouTube** is generously distributed under the *[MIT License](https://opensource.org/licenses/MIT)* 🎉 Enjoy!

## ⚠️ Disclaimer

This script is for educational purposes only. Please ensure you have the right to download any content and comply with YouTube's terms of service when using this script.

<!-- GitHub's Markdown reference links -->
[twitter-icon]: https://img.shields.io/badge/x-000000?style=for-the-badge&logo=x
[github-icon]: https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white
[youtube-icon]: https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white
