#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import subprocess

from . import srs_parser

def launch_mpv(srs_file, level, limit_audio_channels=None):
    content_metadata, streams_metadata, minimal_content_compatibility_level = srs_parser.parseJSON(srs_file)
    srs_file.close()

    CONTENT_TITLE = content_metadata["title"]
    print("TITLE:", CONTENT_TITLE)
    if level > minimal_content_compatibility_level:
        print("Content compatibility error!")
        print("Minimal content compatibility level is {}.".format(minimal_content_compatibility_level))
        exit(1)

    commandline = ["mpv", "--title={}".format(CONTENT_TITLE)]

    if streams_metadata[0] is not None:
        commandline += [streams_metadata[0].get_compatible_files(level)[0]]

    if streams_metadata[1] is not None:
        line = "--audio-files="
        for stream in streams_metadata[1]:
            if limit_audio_channels is not None:
                file = stream.get_file(limit_audio_channels, level)
                if file is not None:
                    line += "{}:".format(file)
                    continue
            files = stream.get_compatible_files(level)
            for file in files:
                line += "{}:".format(file)
        commandline += [line]

    if streams_metadata[2] is not None:
        line = "--sub-files="
        for stream in streams_metadata[2]:
            line += "{}:".format(stream.get_compatible_files(level)[0])
        commandline.append(line)

    print("COMMANDLINE", commandline)

    subprocess.run(commandline)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("SRS_file", help="Stream References Sheet file in JSON format (*.srs.json)", type=open)
    parser.add_argument("--level", help="Target content compatibility level", required=True, type=int)
    parser.add_argument("--limit_audio_channels", type=int)
    args = parser.parse_args()
    print("LEVEL", args.level)

    launch_mpv(args.SRS_file, args.level, args.limit_audio_channels)





