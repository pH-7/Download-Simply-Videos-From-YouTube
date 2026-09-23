#!/usr/bin/env python3
"""
Cleanup script for incomplete YouTube downloads
"""
import os
import re
import glob

# While downloading separate video+audio streams, yt-dlp writes one
# intermediate file per stream, named "<title> [<id>].f<format_id>.<ext>".
# A completed merge removes them, so any that survive are leftovers from
# an interrupted run and are not playable downloads.
#
# Matched by name rather than by glob: a pattern such as "*.f*.mp4" also
# matches an ordinary title containing dots, e.g. "my.favourite.mp4".
# Two or more digits keeps every format id YouTube actually serves
# (18, 140, 251, 313, ...) while leaving a title like "Track.f1.mp3" alone.
INTERMEDIATE_STREAM = re.compile(r"\.f\d{2,}\.[A-Za-z0-9]+$")

MEDIA_EXTENSIONS = ('.mp4', '.mp3', '.mkv', '.webm')

CLEANUP_PATTERNS = (
    "*.part",
    "*.ytdl",
    "*.temp",
    "*.part-Frag*",
)


def _remove(file_path: str, removed: list) -> None:
    """Delete one file, recording its name or reporting the failure."""

    try:
        os.remove(file_path)
        removed.append(os.path.basename(file_path))
        print(f"🗑️  Removed: {os.path.basename(file_path)}")

    except OSError as error:
        print(f"❌ Failed to remove {file_path}: {error}")


def cleanup_incomplete_downloads(downloads_dir="downloads"):
    """
    Clean up incomplete downloads: partial files (.part, .ytdl, .temp)
    and orphaned per-stream intermediates left by an interrupted merge.

    Note that removing .part files discards resume progress, so an
    interrupted download starts over rather than continuing.

    Args:
        downloads_dir (str): Directory to clean

    Returns:
        Tuple[int, int]: (files removed, complete downloads remaining)
    """

    if not os.path.exists(downloads_dir):
        print(f"❌ Downloads directory '{downloads_dir}' not found")
        return 0, 0

    print(f"🧹 Cleaning up incomplete downloads in '{downloads_dir}'...")

    cleaned_files = []

    for pattern in CLEANUP_PATTERNS:
        pattern_path = os.path.join(downloads_dir, "**", pattern)

        for file_path in glob.glob(pattern_path, recursive=True):
            _remove(file_path, cleaned_files)

    for root, _dirs, files in os.walk(downloads_dir):
        for name in files:
            if INTERMEDIATE_STREAM.search(name):
                _remove(os.path.join(root, name), cleaned_files)

    if cleaned_files:
        print(
            f"\n✅ Cleaned up {len(cleaned_files)} "
            f"{'files' if len(cleaned_files) != 1 else 'file'}"
        )

    else:
        print("✅ No incomplete files found")

    complete_count = 0

    for _root, _dirs, files in os.walk(downloads_dir):
        for name in files:
            if (
                name.endswith(MEDIA_EXTENSIONS) and
                not INTERMEDIATE_STREAM.search(name)
            ):
                complete_count += 1

    print(f"\n📁 Complete downloads remaining: {complete_count}")

    return len(cleaned_files), complete_count


if __name__ == "__main__":
    cleanup_incomplete_downloads()
