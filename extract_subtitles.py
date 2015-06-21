#!/usr/bin/env python
# coding: utf-8


"""Extract subtitles from a Matroska file."""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


import argparse
from os import path
import re
import sys

import sh


SUBTITLE_EXTENSION = 'srt'


class Track(object):

    def __init__(self, track_number, language, name):
        self._track_number = track_number
        self._language = language
        self._name = name

    @property
    def number(self):
        return self._track_number

    def __str__(self):
        prefix = 'Track number {}:'.format(self._track_number)

        result = '{} Language: {}\n'.format(prefix, self._language)
        if self._name:
            result += '{} Name: {}'.format(len(prefix) * ' ', self._name)

        return result


class Extractor(object):

    def extract(self, mkv_file):
        info = self._get_info(mkv_file)
        tracks = self._get_tracks(info)
        selected_track = self._ask_for_choice(tracks)
        self._extract_track(mkv_file, selected_track)

    def _get_info(self, mkv_file):
        try:
            return sh.mkvinfo(mkv_file).stdout
        except sh.ErrorReturnCode as error:
            sys.exit(
                '{} exited with code {}'.format(
                    error.full_cmd,
                    error.exit_code
                )
            )

    def _get_tracks(self, info):
        raw_tracks = self._parse_segment(info)
        return self._parse_tracks(raw_tracks)

    def _parse_segment(self, info):

        segment = re.search(
            '^\|\+ Segment tracks\n'
            '^(.*?)'
            '^\|\+ ',
            info,
            re.MULTILINE | re.DOTALL
        ).group(1)

        tracks = segment.split('| + A track\n')

        return filter(None, tracks)

    def _parse_tracks(self, tracks):

        subtitle_tracks = []

        for track in tracks:
            if re.search('Track type: subtitles', track):
                track_num = re.search(
                    'Track number: \d+'
                    ' \(track ID for mkvmerge & mkvextract: (\d+)\)\n',
                    track
                ).group(1)

                language = re.search(
                    'Language: (.+)',
                    track
                ).group(1)

                name_field = re.search(
                    'Name: (.+)',
                    track
                )
                name = name_field.group(1) if name_field else ''

                subtitle_tracks.append(Track(track_num, language, name))

        return subtitle_tracks

    def _ask_for_choice(self, subtitle_tracks):

        for track in subtitle_tracks:
            print(track)

        selected_track = raw_input(
            'Please enter the number of the track to be extracted: '
        )

        if selected_track in [track.number for track in subtitle_tracks]:
            return selected_track
        else:
            sys.exit(
                '{} is not a valid track number. Exiting.'.format(
                    selected_track
                )
            )

    def _extract_track(self, mkv_file, track_number):

        subtitle_file = '{}.{}'.format(
            path.splitext(mkv_file)[0],
            SUBTITLE_EXTENSION
        )

        try:
            for chunk in sh.mkvextract(
                'tracks',
                mkv_file,
                '{}:{}'.format(track_number, subtitle_file),
                _iter=True,
                _out_bufsize=64,
            ):
                sys.stdout.write(chunk)
        except sh.ErrorReturnCode as error:
            sys.exit(
                '{} exited with code {}'.format(
                    error.full_cmd,
                    error.exit_code
                )
            )

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'mkv_file',
        help='the .mkv to extract an .srt from'
    )
    args = parser.parse_args()

    Extractor().extract(args.mkv_file)
