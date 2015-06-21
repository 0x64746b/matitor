Matitor
=======

Matitor is a *Mat*roska Sub*tit*le Extrac*tor*.

It is a thin wrapper around the `mkvtoolnix` binaries. It basically parses the
generic output of `mkvinfo` to present the user with a choice of the subtitle
tracks contained in the `.mkv` and then calls `mkvextract` to generate a `.srt`
file.

This prevents the user from having to parse the output manually. As a side
effect, the script takes care of naming the generated `.srt` exactly as the
`.mkv` it was extracted from and placing the subtitle file next to the video
file.

How
---

```
$ python extract_subtitles.py -h
usage: extract_subtitles.py [-h] mkv_file

Extract subtitles from a Matroska file.

positional arguments:
  mkv_file    the .mkv to extract an .srt from

optional arguments:
  -h, --help  show this help message and exit
$
```

Example
-------

```
$ python extract_subtitles.py my_summer_holidays.mkv
Track number 2: Language: eng
                Name: Foreign Speaking Parts Only
Track number 3: Language: eng
Please enter the number of the track to be extracted: 2
Extracting track 2 with the CodecID 'S_TEXT/UTF8' to the file '/home/dtk/videos/spain_2015/my_summer_holidays.srt'. Container format: SRT text subtitles
Progress: 100%
$
```
