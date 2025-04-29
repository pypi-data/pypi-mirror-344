#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import os
import struct
import sys

if __package__ is None:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from serato_tools.utils.track_tags import check_version, pack_version

GEOB_KEY = "Serato Autotags"

VERSION_BYTES = (0x01, 0x01)


def readbytes(fp: io.BytesIO | io.BufferedReader):
    for x in iter(lambda: fp.read(1), b""):
        if x == b"\00":
            break
        yield x


def parse(fp: io.BytesIO | io.BufferedReader):
    check_version(fp.read(2), VERSION_BYTES)

    for i in range(3):
        data = b"".join(readbytes(fp))
        yield float(data.decode("ascii"))


def dump(bpm: float, autogain: float, gaindb: float):
    data = pack_version(VERSION_BYTES)
    for value, decimals in ((bpm, 2), (autogain, 3), (gaindb, 3)):
        data += "{:.{}f}".format(value, decimals).encode("ascii")
        data += b"\x00"
    return data


if __name__ == "__main__":
    import argparse
    import configparser
    import subprocess
    import tempfile

    import mutagen._file

    from serato_tools.utils.track_tags import get_geob, tag_geob
    from serato_tools.utils.ui import get_text_editor

    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("-e", "--edit", action="store_true")
    args = parser.parse_args()

    tagfile = mutagen._file.File(args.file)
    if tagfile is not None:
        fp = io.BytesIO(get_geob(tagfile, GEOB_KEY))
    else:
        fp = open(args.file, mode="rb")

    with fp:
        bpm, autogain, gaindb = parse(fp)

    if args.edit:
        editor = get_text_editor()

        with tempfile.NamedTemporaryFile() as f:
            f.write(
                (f"bpm: {bpm}\n" "autogain: {autogain}\n" "gaindb: {gaindb}\n").encode(
                    "ascii"
                )
            )
            f.flush()
            status = subprocess.call((editor, f.name))
            f.seek(0)
            output = f.read()

        if status != 0:
            error_str = (f"Command executation failed with status: {status}",)
            print(error_str, file=sys.stderr)
            raise Exception(error_str)

        cp = configparser.ConfigParser()
        try:
            cp.read_string("[Autotags]\n" + output.decode())
            bpm = cp.getfloat("Autotags", "bpm")
            autogain = cp.getfloat("Autotags", "autogain")
            gaindb = cp.getfloat("Autotags", "gaindb")
        except Exception:
            print("Invalid input, no changes made", file=sys.stderr)
            raise

        new_data = dump(bpm, autogain, gaindb)
        if tagfile:
            if tagfile is not None:
                tag_geob(tagfile, GEOB_KEY, new_data)
                tagfile.save()
        else:
            with open(args.file, mode="wb") as fp:
                fp.write(new_data)
    else:
        print(f"BPM: {bpm}")
        print(f"Auto Gain: {autogain}")
        print(f"Gain dB: {gaindb}")
