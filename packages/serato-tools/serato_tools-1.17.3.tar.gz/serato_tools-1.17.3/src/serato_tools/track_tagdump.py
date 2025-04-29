#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import os
import sys
from typing import Generator

import mutagen._file
import mutagen.aiff
import mutagen.flac
import mutagen.mp3
import mutagen.mp4
import mutagen.oggvorbis

if __package__ is None:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def get_serato_tagdata(
    tagfile, decode: bool = False
) -> Generator[tuple[str, bytes | str], None, None]:
    if tagfile and tagfile.tags:
        if isinstance(tagfile, (mutagen.mp3.MP3, mutagen.aiff.AIFF)):
            for tagname, tagvalue in tagfile.tags.items():
                if tagname.startswith("GEOB:Serato "):
                    yield tagname[5:], tagvalue.data
        elif isinstance(tagfile, (mutagen.flac.FLAC, mutagen.mp4.MP4)):
            for tagname, tagvalue in tagfile.tags.items():  # type: ignore
                if not tagname.startswith("serato_") and not tagname.startswith(
                    "----:com.serato.dj:"
                ):
                    continue

                if isinstance(tagfile, mutagen.flac.FLAC):
                    encoded_data = tagvalue[0].encode("utf-8")
                else:
                    encoded_data = bytes(tagvalue[0])

                fixed_data = encoded_data

                length = len(fixed_data.splitlines()[-1])
                if length % 4 == 1:
                    fixed_data += b"A=="
                elif length % 4 == 2:
                    fixed_data += b"=="
                elif length % 4 == 3:
                    fixed_data += b"="
                data = base64.b64decode(fixed_data)

                if not data.startswith(b"application/octet-stream\0"):
                    print(f"Failed to parse tag: {tagname}")
                    continue
                fieldname_endpos = data.index(b"\0", 26)
                fieldname = data[26:fieldname_endpos].decode()
                fielddata = data[fieldname_endpos + 1 :]
                yield fieldname, fielddata if decode else encoded_data
        elif isinstance(tagfile, mutagen.oggvorbis.OggVorbis):
            for tagname, tagvalue in tagfile.tags.items():  # type: ignore
                if not tagname.startswith("serato_"):
                    continue
                yield tagname, tagvalue[0].encode("utf-8")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("input_file")
    parser.add_argument("output_dir", nargs='?')
    parser.add_argument("-d", "--decode", action="store_true")
    args = parser.parse_args()

    tagfile = mutagen._file.File(args.input_file)

    for field, value in get_serato_tagdata(tagfile, decode=args.decode):
        log_str = f'field {field} { "decoded " if args.decode else "" }value: {value}'
        if args.output_dir:
            filename = f"{field}.octet-stream"
            filepath: str | None = (
                os.path.join(args.output_dir, filename) if args.output_dir else None
            )

            print(log_str + f" (written to file {filepath})")
            with open(filepath, mode="wb") as fp:
                fp.write(value)
        else:
            print(log_str)
