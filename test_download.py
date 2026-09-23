"""
Tests for download.py — focused on verifying the format selector
picks high-quality separate streams (not pre-merged low-res ones).

Usage:
    python -m pytest test_download.py -v
    python -m pytest test_download.py -v -k "not slow"   # skip actual download
"""

import os
import subprocess
import tempfile
import unittest

from yt_dlp import YoutubeDL

from download import (
    YOUTUBE_PLAYER_CLIENTS,
    download_single_video,
)

TEST_URL = "https://www.youtube.com/watch?v=K3SR37pIzVs"
TEST_DOWNLOADS_DIR = os.path.join(os.path.dirname(__file__), "test_downloads")

# Default format selector (no resolution limit) - matches download.py
FORMAT_SELECTOR = "bestvideo+bestaudio/best"

# Format selector with max resolution limit
def format_selector_with_limit(max_res: int) -> str:
    return f"bestvideo[height<={max_res}]+bestaudio/best[height<={max_res}]"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _probe_resolution(filepath: str) -> tuple[int, int]:
    """Return (width, height) of a video file using ffprobe."""
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "csv=s=x:p=0",
            filepath,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    width, height = result.stdout.strip().split("x")
    return int(width), int(height)


def _resolve_format(url: str) -> dict:
    """
    Ask yt-dlp which format(s) it would select for our FORMAT_SELECTOR.
    Uses build_format_selector to apply the format string directly to the
    available formats list — no download required.
    Returns a dict with 'info' (raw info) and 'selected' (list of chosen streams).
    """
    opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extractor_args": {
            "youtube": {
                "player_client": YOUTUBE_PLAYER_CLIENTS,
                # player_skip intentionally omitted — it prevents adaptive
                # (separate video+audio) streams from being discovered
            }
        },
        "nocheckcertificate": True,
    }
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
        selector_fn = ydl.build_format_selector(FORMAT_SELECTOR)
        selected = list(selector_fn({"formats": info.get("formats", []), **info}))
        return {"info": info, "selected": selected}


# ---------------------------------------------------------------------------
# Test: format selection (no download — fast)
# ---------------------------------------------------------------------------

class TestFormatSelection(unittest.TestCase):
    """Verify the format selector picks separate high-quality streams."""

    @classmethod
    def setUpClass(cls):
        result = _resolve_format(TEST_URL)
        cls.info = result["info"]
        cls.selected = result["selected"]  # list of streams chosen by FORMAT_SELECTOR

    def test_info_extracted(self):
        """yt-dlp can reach and parse the video."""
        self.assertIsNotNone(self.info)
        self.assertIn("title", self.info)

    def test_uses_separate_streams(self):
        """
        The format selector must pick two separate streams (video + audio)
        rather than a single pre-merged stream.
        """
        self.assertGreaterEqual(
            len(self.selected), 1,
            msg="Format selector returned no matching formats.",
        )
        # Separate-stream selection yields a tuple/group; pre-merged is a single dict
        chosen = self.selected[0]
        if isinstance(chosen, (list, tuple)):
            streams = list(chosen)
        else:
            streams = [chosen]
        self.assertEqual(
            len(streams), 2,
            msg=(
                f"Expected 2 separate streams (video+audio), got {len(streams)}. "
                "A pre-merged stream was likely selected — quality will be lower."
            ),
        )

    def test_video_stream_height(self):
        """Selected video stream must be at least 720p."""
        if not self.selected:
            self.skipTest("No formats selected.")
        chosen = self.selected[0]
        streams = list(chosen) if isinstance(chosen, (list, tuple)) else [chosen]
        video_stream = next(
            (f for f in streams if f.get("vcodec") not in (None, "none")), None
        )
        self.assertIsNotNone(video_stream, "Could not find a video stream.")
        height = video_stream.get("height", 0)
        self.assertGreaterEqual(
            height, 720,
            msg=f"Video stream height is {height}p — expected at least 720p.",
        )

    def test_video_stream_not_premerged_cap(self):
        """
        Selected video stream must NOT be a 360p/480p pre-merged stream
        (the kind that 'best[height<=1080]' used to fall back to).
        """
        if not self.selected:
            self.skipTest("No formats selected.")
        chosen = self.selected[0]
        streams = list(chosen) if isinstance(chosen, (list, tuple)) else [chosen]
        video_stream = next(
            (f for f in streams if f.get("vcodec") not in (None, "none")), None
        )
        self.assertIsNotNone(video_stream)
        height = video_stream.get("height", 0)
        self.assertGreater(
            height, 480,
            msg=f"Stream height {height}p looks like a low-quality pre-merged track.",
        )


class TestFormatSelectionWithLimit(unittest.TestCase):
    """Verify the format selector respects max_resolution limits."""

    @classmethod
    def setUpClass(cls):
        cls.max_res = 720
        opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "extractor_args": {
                "youtube": {
                    "player_client": YOUTUBE_PLAYER_CLIENTS,
                }
            },
            "nocheckcertificate": True,
        }
        with YoutubeDL(opts) as ydl:
            cls.info = ydl.extract_info(TEST_URL, download=False)
            selector_fn = ydl.build_format_selector(format_selector_with_limit(cls.max_res))
            cls.selected = list(selector_fn({"formats": cls.info.get("formats", []), **cls.info}))

    def test_video_stream_respects_limit(self):
        """Selected video stream must not exceed the max_resolution."""
        if not self.selected:
            self.skipTest("No formats selected.")
        chosen = self.selected[0]
        streams = list(chosen) if isinstance(chosen, (list, tuple)) else [chosen]
        video_stream = next(
            (f for f in streams if f.get("vcodec") not in (None, "none")), None
        )
        self.assertIsNotNone(video_stream, "Could not find a video stream.")
        height = video_stream.get("height", 0)
        self.assertLessEqual(
            height, self.max_res,
            msg=f"Video stream height is {height}p — expected at most {self.max_res}p.",
        )


# ---------------------------------------------------------------------------
# Test: actual download + file quality (slow — hits network)
# ---------------------------------------------------------------------------

class TestVideoDownload(unittest.TestCase):
    """Download the video to test_downloads/ and verify the output file."""

    @classmethod
    def setUpClass(cls):
        os.makedirs(TEST_DOWNLOADS_DIR, exist_ok=True)
        cls.result = download_single_video(
            url=TEST_URL,
            output_path=TEST_DOWNLOADS_DIR,
            thread_id=0,
            audio_only=False,
        )
        # Find the downloaded file (first .mp4 in test_downloads/)
        cls.downloaded_file = None
        for fname in os.listdir(TEST_DOWNLOADS_DIR):
            if fname.endswith(".mp4"):
                cls.downloaded_file = os.path.join(TEST_DOWNLOADS_DIR, fname)
                break

    def test_download_succeeds(self):
        """download_single_video must report success."""
        self.assertTrue(
            self.result.get("success"),
            msg=f"Download failed: {self.result.get('message')}",
        )

    def test_file_exists(self):
        """An MP4 file must be created in test_downloads/."""
        self.assertIsNotNone(
            self.downloaded_file,
            msg=f"No .mp4 file found in {TEST_DOWNLOADS_DIR}",
        )
        self.assertTrue(os.path.isfile(self.downloaded_file))

    def test_file_not_empty(self):
        """Downloaded file must be larger than 1 MB (sanity check)."""
        if not self.downloaded_file:
            self.skipTest("No file to check.")
        size_mb = os.path.getsize(self.downloaded_file) / (1024 * 1024)
        self.assertGreater(size_mb, 1, msg=f"File is suspiciously small: {size_mb:.2f} MB")

    def test_resolution_at_least_720p(self):
        """ffprobe must report a height of at least 720px."""
        if not self.downloaded_file:
            self.skipTest("No file to probe.")
        try:
            _, height = _probe_resolution(self.downloaded_file)
        except (subprocess.CalledProcessError, ValueError) as exc:
            self.fail(f"ffprobe failed: {exc}")
        self.assertGreaterEqual(
            height, 720,
            msg=f"Downloaded video is only {height}p — expected at least 720p.",
        )


if __name__ == "__main__":
    unittest.main()
