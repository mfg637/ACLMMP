#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import subprocess

import srs_parser

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("SRS_file", help="Stream References Sheet file in JSON format (*.srs.json)", type=open)
    parser.add_argument("--level", help="Target content compatibility level", required=True, type=int)
    parser.add_argument("--limit_audio_channels", type=int)
    args = parser.parse_args()
    print("LEVEL", args.level)

    content_metadata, streams_metadata, minimal_content_compatibility_level = srs_parser.parseJSON(args.SRS_file)
    args.SRS_file.close()

    CONTENT_TITLE = content_metadata["title"]
    print("TITLE:", CONTENT_TITLE)
    if args.level > minimal_content_compatibility_level:
        print("Content compatibility error!")
        print("Minimal content compatibility level is {}.".format(minimal_content_compatibility_level))
        exit(1)

    commandline = ["mpv", "--title={}".format(CONTENT_TITLE)]

    if streams_metadata[0] is not None:
        commandline += [streams_metadata[0].get_compatible_files(args.level)[0]]

    if streams_metadata[1] is not None:
        line = "--audio-files="
        for stream in streams_metadata[1]:
            def cl_add_file():
                global line
                line += "{}:".format(file)
            if args.limit_audio_channels is not None:
                file = stream.get_file(args.limit_audio_channels, args.level)
                if file is not None:
                    cl_add_file()
                    continue
            files = stream.get_compatible_files(args.level)
            for file in files:
                cl_add_file()
        commandline += [line]

    if streams_metadata[2] is not None:
        line = "--sub-files="
        for stream in streams_metadata[2]:
            line += "{}:".format(stream.get_compatible_files(args.level)[0])
        commandline.append(line)

    print(commandline)

    subprocess.run(commandline)




