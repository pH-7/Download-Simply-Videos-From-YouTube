# 📥 Download Any Videos From YouTube

**⚡️ High-Quality YouTube Video, Playlist & Channel Downloader 🎥**

![Demo. Download any YouTube videos and YouTube playlists](promo-assets/demo-download-youtube-videos-script.gif)

> [!Note]
>
> #### 🚀 The Ultimate YouTube Downloader
> 
> Download any YouTube video, playlist, or entire channel just by pasting a URL. Videos are saved to your computer in high quality — no account or sign-in needed.

**What you can do:**
- 🎥 Download any YouTube video as MP4
- 🎵 Download audio-only as MP3 (great for music and podcasts)
- 📋 Download entire playlists — each saved in its own numbered folder
- 📺 Download a whole YouTube channel
- ⚡ Download multiple videos or playlists at the same time

- [🚀 Quick Start](#-quick-start)
- [🪄 Usage](#-usage)
- [🎵 Playlist Downloads](#-playlist-downloads)
- [📺 Channel Downloads](#-channel-downloads)
- [🧹 Clean Up Incomplete Downloads](#-optional-clean-up-incomplete-downloads)
- [📦 Full Setup (for developers)](#-full-setup-for-developers)
- [🛠️ Advanced Options](#%EF%B8%8F-advanced-options)
- [👨‍🍳 Who made this?](#-who-cooked-this)
- [🤝 Contributing](#-contributing)
- [⚖️ License](#%EF%B8%8F-license)

## 🚀 Quick Start

> New here? Follow these steps and you'll be downloading videos in a few minutes.

### Step 1 — Install Python

[Download Python 3.10 or newer](https://www.python.org/downloads/) and install it.

> **Windows users:** during installation, tick the **"Add Python to PATH"** checkbox at the bottom of the first screen — easy to miss!

### Step 2 — Install FFmpeg

FFmpeg is a free tool that handles saving and converting video files.

- **macOS** — open Terminal and run:
  ```bash
  brew install ffmpeg
  ```
  > Don't have Homebrew? [Install it here](https://brew.sh) first (one command, takes about a minute).

- **Windows** — [download FFmpeg here](https://ffmpeg.org/download.html), unzip it, and add it to your PATH. ([step-by-step guide](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/))

- **Linux (Ubuntu/Debian)** — open a terminal and run:
  ```bash
  sudo apt-get install ffmpeg
  ```

### Step 3 — Download this project

Click the green **Code** button at the top of this page → **Download ZIP**. Unzip it anywhere you like (your Desktop is fine).

### Step 4 — Open a terminal inside the project folder

- **macOS:** right-click the unzipped folder → **New Terminal at Folder**
- **Windows:** open the folder, click the address bar at the top, type `cmd`, press Enter
- **Linux:** right-click the folder → **Open Terminal**

### Step 5 — Install the required libraries

In the terminal, run these three commands one by one:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> **Windows:** use `venv\Scripts\activate` instead of `source venv/bin/activate`.

That's it — you're ready! See [Usage](#-usage) below.

> **Each time you open a new terminal**, you must run `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows) before using the script.

## 🪄 Usage

> **First, make sure your virtual environment is active.** If you see `(venv)` at the start of your terminal prompt, you're good. If not, run:
> ```bash
> source venv/bin/activate
> ```
> (Windows: `venv\Scripts\activate`)

In your terminal, run:

```bash
python download.py
```

You'll be asked for a YouTube URL. Paste it and press Enter — that's it!

```
Enter YouTube URL(s): https://www.youtube.com/watch?v=Hhb8ghB8lMg
```

Your video will be saved in the `downloads/` folder.

### Download multiple videos at once

Paste multiple URLs separated by commas:

```
Enter YouTube URL(s): https://youtu.be/abc123, https://youtu.be/def456, https://youtu.be/ghi789
```

Or press Enter on an empty prompt to switch to one-URL-per-line mode:

```
Enter YouTube URL(s): [press Enter]
📝 Multi-line mode activated!
   URL 1: https://youtu.be/abc123
   URL 2: https://youtu.be/def456
   URL 3: [press Enter again to finish]
```

You can freely mix videos, playlists, and channel URLs in the same command — the script handles each one correctly.

> **If one URL fails, the rest keep downloading.** A dead link or private video won't stop your other downloads.

### Download audio only (MP3) 🎵

When the script asks for a format, choose option `2`:

```
Choose format:
  1. MP4 Video (default)
  2. MP3 Audio only
Enter choice (1-2, default=1): 2
```

Great for music playlists, podcasts, and lectures.

## 🎵 Playlist Downloads

Paste a playlist URL and every video in it will be downloaded and saved in its own folder:

```
Enter YouTube URL(s): https://www.youtube.com/playlist?list=PLxxxxxxx
```

You can download multiple playlists at once by separating their URLs with commas.

MP3 mode works with playlists too — all audio files are saved in the same numbered folder structure.

**📁 Example result:**
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

Paste any YouTube channel URL to download all its videos:

```
Enter YouTube URL(s): https://www.youtube.com/@channelname
```

All these URL formats work automatically:
- `https://www.youtube.com/@channelname`
- `https://www.youtube.com/channel/UCxxxxxxxxx`
- `https://www.youtube.com/c/channelname`
- `https://www.youtube.com/user/username`

Videos are saved in a folder named after the channel, sorted by upload date.

MP3 mode works for channels too — useful for music or podcast channels to save disk space.

> **Heads up:** channels with hundreds of videos can take a long time to download. The script paces requests automatically to avoid being blocked by YouTube.

**📁 Channel file structure example:**
```
downloads/
├── TechChannel/
│   ├── 20240815-Latest Tech Review.mp4
│   ├── 20240810-Programming Tutorial.mp4
│   └── 20240805-Tech News Update.mp4
└── Individual Video.mp4
```

## 🧹 Optional: Clean Up Incomplete Downloads

If a download was interrupted (e.g. you lost internet or closed the terminal), some unfinished files may be left in the `downloads/` folder. To remove them, run:

```bash
python cleanup_downloads.py # python3 cleanup_downloads.py
```

This only deletes incomplete files (`.part`, `.ytdl`, temp fragments) — your finished downloads are untouched. No need to activate the virtual environment for this; it uses no external dependencies. Most people will never need this.

---

## 📦 Full Setup (for developers)

If you're comfortable with the command line or want to contribute to the project:

1. **Clone the repository**

   ```bash
   git clone https://github.com/pH-7/Download-Simply-Videos-From-YouTube.git
   cd Download-Simply-Videos-From-YouTube
   ```

2. **Create a virtual environment** *(keeps this project's packages separate from your system)*

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   > **Windows:** use `venv\Scripts\activate` instead.
   > Run this activation command again each time you open a new terminal.

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install FFmpeg** — see [Step 2 of Quick Start](#step-2--install-ffmpeg) above.

---

## 🛠️ Advanced Options

### List available formats for a video

To see all quality options for a specific video before downloading:

```bash
python download.py --list-formats
```

### Control how many downloads run at the same time

The script supports simultaneous downloads. When downloading multiple videos, you'll be asked how many to run in parallel (1–5, default is 3). More = faster, but uses more bandwidth.

```
Number of concurrent downloads (1-5, default=3): 5
```

### Customise the script

You can edit `download.py` to change:
- Maximum video resolution (currently capped at 1080p)
- Default output folder
- Number of retry attempts for failed downloads

## 👨‍🍳 Who cooked this?

[![Pierre-Henry Soria](https://s.gravatar.com/avatar/a210fe61253c43c869d71eaed0e90149?s=200)](https://PH7.me 'Pierre-Henry Soria personal website')

**Pierre-Henry Soria**. A passionate **software AI engineer** who loves automating content creation! 🚀 Enthusiast for YouTube, photography, AI, learning, and health! 😊 Find me at [pH7.me](https://ph7.me) 🚀

☕️ Do you enjoy this project? **[Offer me a coffee](https://ko-fi.com/phenry)** (spoiler alert: I love almond flat white! 😋)

[![@phenrysay][x-icon]](https://x.com/phenrysay "Follow Me on X") [![pH-7][github-icon]](https://github.com/pH-7 "Follow Me on GitHub") [![YouTube Tech Videos][youtube-icon]](https://www.youtube.com/@pH7Programming "My YouTube Tech Channel") [![BlueSky][bsky-icon]](https://bsky.app/profile/ph7.me "Follow Me on BlueSky")

## 🤝 Contributing

Fork the repo and submit a pull request.

## ⚖️ License

**Download Simply Videos From YouTube** is generously distributed under the *[MIT License](https://opensource.org/licenses/MIT)* 🎉 Enjoy!

## ⚠️ Disclaimer

This script is for educational purposes only. Before using this script, please **ensure you have the right to download the content and that you comply with YouTube's terms of service**.

<!-- GitHub's Markdown reference links -->
[x-icon]: https://img.shields.io/badge/x-000000?style=for-the-badge&logo=x
[bsky-icon]: https://img.shields.io/badge/BlueSky-00A8E8?style=for-the-badge&logo=bluesky&logoColor=white
[github-icon]: https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white
[youtube-icon]: https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white
