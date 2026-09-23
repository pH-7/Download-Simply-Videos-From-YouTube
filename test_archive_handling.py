"""Unit tests for download archive result handling."""

import io
import tempfile
import unittest
from pathlib import Path
from contextlib import redirect_stdout
from unittest.mock import MagicMock, patch

from download import (
    count_archived_entries,
    download_single_video,
    download_youtube_content,
)


class TestDownloadArchiveHandling(unittest.TestCase):

    @patch('download.YoutubeDL')
    @patch('download.get_url_info')
    def test_archived_video_is_a_successful_skip(
        self,
        get_url_info,
        youtube_dl,
    ):
        video_info = {
            'id': 'already-downloaded',
            'title': 'Existing Video',
            'extractor_key': 'Youtube',
        }
        get_url_info.return_value = ('video', video_info)

        ydl = MagicMock()
        ydl.in_download_archive.return_value = True
        youtube_dl.return_value.__enter__.return_value = ydl

        with tempfile.TemporaryDirectory() as output_path:
            result = download_single_video(
                'https://www.youtube.com/watch?v=already-downloaded',
                output_path,
                thread_id=1,
            )

        self.assertTrue(result['success'])
        self.assertTrue(result['skipped'])
        self.assertEqual(result['count'], 0)
        self.assertIn('already downloaded', result['message'])
        ydl.extract_info.assert_not_called()

    @patch('download.get_url_info')
    def test_real_archive_respects_audio_and_video_separation(self, get_url_info):
        info = {'id': 'archived', 'title': 'Archived', 'extractor_key': 'Youtube'}
        get_url_info.return_value = ('video', info)
        with tempfile.TemporaryDirectory() as output_path:
            Path(output_path, '.video_download_archive').write_text('youtube archived\n')
            with patch('download.YoutubeDL.extract_info') as extract_info:
                video = download_single_video('https://youtu.be/archived', output_path)
                self.assertTrue(video['skipped'])
                extract_info.assert_not_called()
                extract_info.return_value = info
                audio = download_single_video(
                    'https://youtu.be/archived', output_path, audio_only=True,
                )
                self.assertTrue(audio['success'])
                self.assertFalse(audio.get('skipped', False))
                extract_info.assert_called_once()

    @patch('download.time.sleep')
    @patch('download.YoutubeDL')
    @patch('download.get_url_info')
    def test_none_result_still_fails_when_video_is_not_archived(
        self,
        get_url_info,
        youtube_dl,
        sleep,
    ):
        get_url_info.return_value = (
            'video',
            {
                'id': 'unavailable',
                'title': 'Unavailable Video',
                'extractor_key': 'Youtube',
            },
        )

        ydl = MagicMock()
        ydl.in_download_archive.return_value = False
        ydl.extract_info.return_value = None
        youtube_dl.return_value.__enter__.return_value = ydl

        with tempfile.TemporaryDirectory() as output_path:
            result = download_single_video(
                'https://www.youtube.com/watch?v=unavailable',
                output_path,
            )

        self.assertFalse(result['success'])
        self.assertEqual(ydl.extract_info.call_count, 3)
        self.assertEqual(sleep.call_count, 2)

    @patch('download.download_single_video')
    @patch('download.get_content_type', return_value='video')
    def test_summary_reports_skip_separately(
        self,
        get_content_type,
        download_single_video,
    ):
        download_single_video.return_value = {
            'url': 'https://www.youtube.com/watch?v=existing',
            'success': True,
            'count': 0,
            'skipped': True,
            'message': 'already downloaded',
        }

        output = io.StringIO()

        with tempfile.TemporaryDirectory() as output_path:
            with redirect_stdout(output):
                download_youtube_content(
                    ['https://www.youtube.com/watch?v=existing'],
                    output_path=output_path,
                    max_workers=1,
                )

        summary = output.getvalue()
        self.assertIn('Successful downloads: 0 files', summary)
        self.assertIn('Failed downloads: 0 files', summary)
        self.assertIn('Already downloaded: 1 item skipped', summary)
        self.assertIn('No new downloads needed', summary)

    @patch('download.download_single_video')
    @patch('download.get_content_type', return_value='video')
    def test_summary_counts_failed_url_even_when_file_count_is_unknown(
        self,
        get_content_type,
        download_single_video,
    ):
        download_single_video.return_value = {
            'url': 'https://www.youtube.com/watch?v=unavailable',
            'success': False,
            'count': 0,
            'message': 'download failed',
        }

        output = io.StringIO()

        with tempfile.TemporaryDirectory() as output_path:
            with redirect_stdout(output):
                download_youtube_content(
                    ['https://www.youtube.com/watch?v=unavailable'],
                    output_path=output_path,
                    max_workers=1,
                )

        self.assertIn('Failed downloads: 1 file', output.getvalue())


class TestArchivedPlaylistHandling(unittest.TestCase):
    """
    yt-dlp omits archived entries from a playlist result entirely, so a
    fully-downloaded playlist looks empty. It must not be reported as a
    failure -- but a genuinely empty one still must be.
    """

    def _run(self, entries, archived_count):
        ydl = MagicMock()
        ydl.in_download_archive.return_value = False
        ydl.extract_info.return_value = {
            '_type': 'playlist',
            'title': 'Some Playlist',
            'entries': entries,
        }

        with patch('download.YoutubeDL') as youtube_dl, \
                patch('download.get_url_info', return_value=('playlist', {'id': 'pl'})), \
                patch('download.count_archived_entries', return_value=archived_count), \
                patch('download.time.sleep'):
            youtube_dl.return_value.__enter__.return_value = ydl

            with tempfile.TemporaryDirectory() as output_path:
                return download_single_video(
                    'https://www.youtube.com/playlist?list=pl',
                    output_path,
                )

    def test_fully_archived_playlist_is_a_skip_not_a_failure(self):
        result = self._run([], archived_count=19)

        self.assertTrue(result['success'])
        self.assertTrue(result['skipped'])
        self.assertEqual(result['count'], 0)
        self.assertIn('19 archived entries', result['message'])

    def test_archived_playlist_with_unavailable_entries_notes_both(self):
        result = self._run([None], archived_count=4)

        self.assertTrue(result['skipped'])
        self.assertIn('4 archived entries', result['message'])
        self.assertIn('1 unavailable', result['message'])

    def test_genuinely_empty_playlist_still_fails(self):
        result = self._run([], archived_count=0)

        self.assertFalse(result['success'])
        self.assertIn('empty or unavailable', result['message'])

    def test_all_entries_unavailable_still_fails(self):
        result = self._run([None, None, None], archived_count=0)

        self.assertFalse(result['success'])
        self.assertIn('empty or unavailable', result['message'])

    def test_partial_playlist_still_reports_success(self):
        result = self._run([{'id': 'a'}, None], archived_count=0)

        self.assertTrue(result['success'])
        self.assertFalse(result.get('skipped', False))
        self.assertEqual(result['count'], 1)


class TestCountArchivedEntries(unittest.TestCase):

    def test_counts_only_entries_present_in_the_archive(self):
        flat = {'entries': [{'id': 'a'}, {'id': 'b'}, None, {'id': 'c'}]}
        ydl = MagicMock()
        ydl.in_download_archive.side_effect = lambda e: e['id'] in ('a', 'c')

        with patch('download.YoutubeDL') as youtube_dl:
            youtube_dl.return_value.__enter__.return_value.extract_info.return_value = flat
            self.assertEqual(count_archived_entries('https://x', ydl), 2)

    def test_probe_failure_is_not_fatal(self):
        ydl = MagicMock()

        with patch('download.YoutubeDL') as youtube_dl:
            youtube_dl.return_value.__enter__.return_value.extract_info.side_effect = OSError('net')
            self.assertEqual(count_archived_entries('https://x', ydl), 0)


if __name__ == '__main__':
    unittest.main()
