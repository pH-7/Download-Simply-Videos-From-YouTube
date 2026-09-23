#!/usr/bin/env python3
"""
Cleanup script for incomplete YouTube downloads
"""
import os
import glob


def cleanup_incomplete_downloads(downloads_dir="downloads"):
    """Clean up incomplete download files (.part, .ytdl, .temp files)"""

    if not os.path.exists(downloads_dir):
        print(f"❌ Downloads directory '{downloads_dir}' not found")
        return

    print(f"🧹 Cleaning up incomplete downloads in '{downloads_dir}'...")

    # Patterns for incomplete files
    cleanup_patterns = [
        "*.part",
        "*.ytdl",
        "*.temp",
        "*.part-Frag*",
        "*.f*.mp4.part*",
        "*.f*.mp4.ytdl"
    ]

    cleaned_files = []

    for pattern in cleanup_patterns:
        pattern_path = os.path.join(downloads_dir, "**", pattern)
        files = glob.glob(pattern_path, recursive=True)

        for file_path in files:
            try:
                os.remove(file_path)
                cleaned_files.append(os.path.basename(file_path))
                print(f"🗑️  Removed: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"❌ Failed to remove {file_path}: {e}")

    if cleaned_files:
        print(f"\n✅ Cleaned up {len(cleaned_files)} incomplete files")
    else:
        print("✅ No incomplete files found")

    # Show remaining files
    complete_files = []
    for root, dirs, files in os.walk(downloads_dir):
        for file in files:
            if file.endswith(('.mp4', '.mp3', '.mkv', '.webm')):
                complete_files.append(file)

    print(f"\n📁 Complete downloads remaining: {len(complete_files)}")

    return len(cleaned_files), len(complete_files)


if __name__ == "__main__":
    cleanup_incomplete_downloads()
