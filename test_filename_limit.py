"""
Unit tests for filename length limiting.

ext4 and most Linux filesystems reject a filename over 255 bytes. The
name that matters is not the final one: while downloading separate
video+audio streams yt-dlp writes a longer intermediate,
"<base>.f<format_id>.<ext>.part", and "-Frag<n>" on top of that for
fragmented streams. Trimming must leave room for those.
"""

import os
import unittest

from yt_dlp import YoutubeDL

from download import (
    FilenameLengthLimiter,
    MAX_FILENAME_BYTES,
    truncate_to_bytes,
)

VIDEO_TMPL = '%(title)s [%(id)s].%(ext)s'
PLAYLIST_TMPL = '%(playlist_index)03d-%(title)s [%(id)s].%(ext)s'


def _trim(title, outtmpl=VIDEO_TMPL, **extra):
    """Run the limiter over a title, returning (new_title, base_name)."""

    info = {
        'id': 'K3SR37pIzVs',
        'title': title,
        'ext': 'mp4',
        'extractor': 'youtube',
        'extractor_key': 'Youtube',
        'webpage_url': 'https://example.invalid/watch',
        **extra,
    }

    with YoutubeDL({'quiet': True, 'no_warnings': True, 'outtmpl': outtmpl}) as ydl:
        limiter = FilenameLengthLimiter()
        limiter.set_downloader(ydl)
        limiter.run(info)
        base = os.path.splitext(os.path.basename(ydl.prepare_filename(info)))[0]

    return info['title'], base


def _worst_case_bytes(base):
    """The longest name yt-dlp actually writes for this base."""

    return len(f'{base}.f313.webm.part-Frag1234'.encode('utf-8'))


class TestTruncateToBytes(unittest.TestCase):

    def test_leaves_short_text_alone(self):
        self.assertEqual(truncate_to_bytes('hello', 50), 'hello')

    def test_never_splits_a_multibyte_character(self):
        # Each of these is 3 bytes, so a 4-byte budget must drop the second
        result = truncate_to_bytes('日日', 4)

        self.assertEqual(result, '日')
        result.encode('utf-8').decode('utf-8')  # must not raise

    def test_zero_budget_yields_empty(self):
        self.assertEqual(truncate_to_bytes('anything', 0), '')


class TestFilenameLengthLimiter(unittest.TestCase):

    def test_normal_title_is_untouched(self):
        title = 'A Perfectly Normal Video Title'
        result, _base = _trim(title)

        self.assertEqual(result, title)

    def test_long_ascii_title_fits_the_real_intermediate_name(self):
        _result, base = _trim('A' * 400)

        self.assertLessEqual(_worst_case_bytes(base), MAX_FILENAME_BYTES)

    def test_long_multibyte_title_fits_and_stays_decodable(self):
        result, base = _trim('日' * 300)

        self.assertLessEqual(_worst_case_bytes(base), MAX_FILENAME_BYTES)
        result.encode('utf-8').decode('utf-8')

    def test_playlist_prefix_is_accounted_for(self):
        """
        A playlist name carries an index prefix, so less of the budget is
        left for the title. The limiter must not have to know that.
        """
        _flat, flat_base = _trim('C' * 400)
        _listed, listed_base = _trim(
            'C' * 400, outtmpl=PLAYLIST_TMPL, playlist_index=7
        )

        self.assertLessEqual(_worst_case_bytes(listed_base), MAX_FILENAME_BYTES)
        self.assertLess(
            len(listed_base.encode()) - len('007-'),
            len(flat_base.encode()),
            'the prefixed name should leave the title less room',
        )

    def test_empty_title_is_not_touched(self):
        result, _base = _trim('')

        self.assertEqual(result, '')

    def test_title_is_never_emptied(self):
        """Even an extreme case must leave something to name the file."""
        result, _base = _trim('D' * 5000)

        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
