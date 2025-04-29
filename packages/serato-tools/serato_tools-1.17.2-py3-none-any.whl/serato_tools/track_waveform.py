#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import os
import struct
import sys
from typing import Generator

if __package__ is None:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from serato_tools.utils.track_tags import check_version

GEOB_KEY = "Serato Overview"

VERSION_BYTES = (0x01, 0x05)


def parse(fp: io.BytesIO | io.BufferedReader):
    check_version(fp.read(2), VERSION_BYTES)

    for x in iter(lambda: fp.read(16), b""):
        assert len(x) == 16
        yield bytearray(x)


def draw_waveform(data: Generator[bytearray, None, None]):
    from PIL import Image, ImageColor

    img = Image.new("RGB", (240, 16), "black")
    pixels = img.load()

    for i in range(img.size[0]):
        rowdata = next(data)
        factor = len([x for x in rowdata if x < 0x80]) / len(rowdata)

        for j, value in enumerate(rowdata):
            # The algorithm to derive the colors from the data has no real
            # mathematical background and was found by experimenting with
            # different values.
            color = "hsl({hue:.2f}, {saturation:d}%, {luminance:.2f}%)".format(
                hue=(factor * 1.5 * 360) % 360,
                saturation=40,
                luminance=(value / 0xFF) * 100,
            )
            pixels[i, j] = ImageColor.getrgb(color)  # type: ignore

    return img


if __name__ == "__main__":
    import argparse

    import mutagen._file

    from serato_tools.utils.track_tags import get_geob

    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    tagfile = mutagen._file.File(args.file)
    if tagfile is not None:
        fp = io.BytesIO(get_geob(tagfile, GEOB_KEY))
    else:
        fp = open(args.file, mode="rb")

    with fp:
        data = parse(fp)
        img = draw_waveform(data)

    img.show()
