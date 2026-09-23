"""Unit tests for incomplete-download cleanup."""

import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from cleanup_downloads import cleanup_incomplete_downloads


class CleanupTestCase(unittest.TestCase):

    def _run(self, names):
        """Create each name under a temp dir, clean it, return (result, remaining)."""

        with tempfile.TemporaryDirectory() as downloads_dir:

            for name in names:
                path = Path(downloads_dir, name)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('x')

            with redirect_stdout(io.StringIO()):
                result = cleanup_incomplete_downloads(downloads_dir)

            remaining = sorted(
                os.path.relpath(os.path.join(root, name), downloads_dir)
                for root, _dirs, files in os.walk(downloads_dir)
                for name in files
            )

            return result, remaining


class TestPartialFileRemoval(CleanupTestCase):

    def test_removes_partial_and_sidecar_files(self):
        _result, remaining = self._run([
            'Video [a].mp4.part',
            'Video [a].mp4.ytdl',
            'Video [a].mp4.temp',
        ])

        self.assertEqual(remaining, [])

    def test_keeps_finished_downloads(self):
        _result, remaining = self._run(['Video [a].mp4', 'Audio [b].mp3'])

        self.assertEqual(remaining, ['Audio [b].mp3', 'Video [a].mp4'])


class TestOrphanedStreamRemoval(CleanupTestCase):
    """
    An interrupted merge leaves a *complete* per-stream file with no
    .part suffix. It is not playable, and must not be counted as a
    finished download.
    """

    def test_removes_orphaned_stream_left_by_interrupted_merge(self):
        result, remaining = self._run([
            'Talk [K3SR37pIzVs].f313.webm',
            'Talk [K3SR37pIzVs].f251.webm.part',
        ])

        self.assertEqual(remaining, [])
        self.assertEqual(result, (2, 0))

    def test_orphaned_stream_is_not_counted_as_complete(self):
        result, _remaining = self._run([
            'Talk [a].f313.webm',
            'Real Video [b].mp4',
        ])

        removed, complete = result
        self.assertEqual(removed, 1)
        self.assertEqual(complete, 1, 'only the real .mp4 is a finished download')

    def test_removes_orphaned_streams_inside_playlist_folders(self):
        _result, remaining = self._run([
            os.path.join('My Playlist', '001-Song [a].f140.m4a'),
            os.path.join('My Playlist', '001-Song [a].mp3'),
        ])

        self.assertEqual(remaining, [os.path.join('My Playlist', '001-Song [a].mp3')])


class TestTitlesAreNotMistakenForStreams(CleanupTestCase):
    """Deleting a viewer's finished download would be far worse than
    leaving an orphan behind, so the match must stay narrow."""

    def test_keeps_title_containing_dots(self):
        _result, remaining = self._run(['my.favourite.mp4'])

        self.assertEqual(remaining, ['my.favourite.mp4'])

    def test_keeps_title_with_single_digit_f_segment(self):
        _result, remaining = self._run(['Track.f1.mp3'])

        self.assertEqual(remaining, ['Track.f1.mp3'])


class TestMissingDirectory(unittest.TestCase):

    def test_returns_zero_counts_rather_than_none(self):
        with redirect_stdout(io.StringIO()):
            result = cleanup_incomplete_downloads(
                os.path.join(tempfile.gettempdir(), 'definitely-not-here-xyz')
            )

        self.assertEqual(result, (0, 0))


if __name__ == '__main__':
    unittest.main()
