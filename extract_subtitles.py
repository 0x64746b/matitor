#!/usr/bin/env python
# coding: utf-8


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


from os import path
import re
import sys

import sh


MKV_FILE = '<matroska file to extract subtitles from>'
SUBTITLE_EXTENSION = 'srt'


if __name__ == '__main__':

    subtitle_tracks = []

    try:
        mkvinfo = sh.mkvinfo(MKV_FILE)
    except sh.ErrorReturnCode as error:
        sys.exit(
            '{} exited with code {}'.format(error.full_cmd, error.exit_code)
        )

    segment_tracks = re.search(
        '^\|\+ Segment tracks\n'
        '^(.*?)'
        '^\|\+ ',
        mkvinfo.stdout,
        re.MULTILINE | re.DOTALL
    ).group(1)

    tracks = segment_tracks.split('| + A track\n')
    tracks = filter(None, tracks)

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

            prefix = 'Track number {}:'.format(track_num)

            print('{} Language: {}'.format(prefix, language))
            if name:
                print('{} Name: {}'.format(len(prefix) * ' ', name))

            subtitle_tracks.append(track_num)

    selected_track = raw_input(
        'Please enter the number of the track to be extracted: '
    )

    if selected_track not in subtitle_tracks:
        sys.exit(
            '{} is not a valid track number. Exiting.'.format(selected_track)
        )

    subtitle_file = '{}.{}'.format(
        path.splitext(MKV_FILE)[0],
        SUBTITLE_EXTENSION
    )

    try:
        sh.mkvextract(
            'tracks',
            MKV_FILE,
            '{}:{}'.format(selected_track, subtitle_file)
        )
    except sh.ErrorReturnCode as error:
        sys.exit(
            '{} exited with code {}'.format(error.full_cmd, error.exit_code)
        )
    else:
        print(
            'Successfully extracted track {} to {}'.format(
                selected_track,
                subtitle_file
            )
        )
