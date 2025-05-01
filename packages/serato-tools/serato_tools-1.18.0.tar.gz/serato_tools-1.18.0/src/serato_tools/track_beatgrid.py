#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import collections
import io
import os
import struct
import sys

if __package__ is None:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from serato_tools.utils.track_tags import check_version, pack_version

GEOB_KEY = "Serato BeatGrid"

VERSION_BYTES = (0x01, 0x00)

NonTerminalBeatgridMarker = collections.namedtuple(
    "NonTerminalBeatgridMarker",
    ("position", "beats_till_next_marker"),
)
TerminalBeatgridMarker = collections.namedtuple(
    "TerminalBeatgridMarker",
    ("position", "bpm"),
)

Footer = collections.namedtuple("Footer", ("unknown",))

DataType = list[NonTerminalBeatgridMarker | TerminalBeatgridMarker | Footer]


def _check_data(data: DataType):
    nonterminal_markers: list[NonTerminalBeatgridMarker] = []
    terminal_markers: list[TerminalBeatgridMarker] = []
    footers: list[Footer] = []

    for d in data:
        if isinstance(d, NonTerminalBeatgridMarker):
            nonterminal_markers.append(d)
        elif isinstance(d, TerminalBeatgridMarker):
            terminal_markers.append(d)
        elif isinstance(d, Footer):
            footers.append(d)
        else:
            raise TypeError(f"unexpected value type {d}")

    assert (
        len(terminal_markers) == 1
    ), f"should only be 1 terminal marker, but #: {len(terminal_markers)}"
    assert len(footers) == 1, f"should only be 1 footer, but #: {len(footers)}"
    assert isinstance(data[-1], Footer), "last item should be a footer"
    assert isinstance(
        data[-2], TerminalBeatgridMarker
    ), "last item should be a terminal marker"
    return nonterminal_markers, terminal_markers, footers[0]


def parse(fp: io.BytesIO | io.BufferedReader):
    check_version(fp.read(2), VERSION_BYTES)

    num_markers = struct.unpack(">I", fp.read(4))[0]
    for i in range(num_markers):
        position = struct.unpack(">f", fp.read(4))[0]
        data = fp.read(4)
        if i == num_markers - 1:
            bpm = struct.unpack(">f", data)[0]
            yield TerminalBeatgridMarker(position, bpm)
        else:
            beats_till_next_marker = struct.unpack(">I", data)[0]
            yield NonTerminalBeatgridMarker(position, beats_till_next_marker)

    # TODO: What's the meaning of the footer byte?
    yield Footer(struct.unpack("B", fp.read(1))[0])
    assert fp.read() == b""


def write(
    data: DataType,
    fp: io.BytesIO | io.BufferedWriter,
):
    nonterminal_markers, terminal_markers, footer = _check_data(data)
    markers = nonterminal_markers + terminal_markers
    # Write version
    fp.write(pack_version(VERSION_BYTES))

    # Write markers
    fp.write(struct.pack(">I", len(markers)))
    for marker in markers:
        fp.write(struct.pack(">f", marker.position))
        if isinstance(marker, TerminalBeatgridMarker):
            fp.write(struct.pack(">f", marker.bpm))
        elif isinstance(marker, NonTerminalBeatgridMarker):
            fp.write(struct.pack(">I", marker.beats_till_next_marker))
        else:
            raise TypeError(f"Unexpected marker type: {type(marker)}")

    # Write footer
    fp.write(struct.pack("B", footer.unknown))


def analyze_and_write(file: str):
    import mutagen._file

    from serato_tools.utils.beatgrid_analyze import analyze_beatgrid
    from serato_tools.utils.track_tags import tag_geob

    tagfile = mutagen._file.File(file)
    assert tagfile, "file parse failed"
    bpm = float(str(tagfile["TBPM"]))

    print("Analyzing beat grid...")
    beat_analyzer = analyze_beatgrid(file, bpm_helper=bpm)

    print("Writing tags...")
    markers: DataType = [
        NonTerminalBeatgridMarker(position, 4)
        for position in beat_analyzer.downbeats[:-1]
    ] + [
        TerminalBeatgridMarker(
            beat_analyzer.downbeats[-1], bpm=bpm or beat_analyzer.bpm
        ),
        Footer(0),
    ]

    fpw = io.BytesIO()
    write(markers, fpw)
    fpw.seek(0)
    new_data = fpw.read()

    tag_geob(tagfile, GEOB_KEY, new_data)
    tagfile.save()


def main():
    import argparse

    import mutagen._file

    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    tagfile = mutagen._file.File(args.file)
    if tagfile is not None:
        analyze_and_write(args.file)
    else:
        fp = open(args.file, mode="rb")

        with fp:
            for marker in parse(fp):
                print(marker)


if __name__ == "__main__":
    main()
