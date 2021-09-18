#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import pathlib
import subprocess

import srs_parser

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("SRS_file", help="Stream References Sheet file in JSON format (*.srs.json)", type=open)
    parser.add_argument("--level", help="Target content compatibility level", required=True, type=int)
    parser.add_argument("-o", help="Output file name", type=pathlib.Path)
    parser.add_argument("--limit_audio_channels", type=int)
    parser.add_argument("--webm", help="enable webm compatibility and muxing", action='store_true')
    args = parser.parse_args()
    print("LEVEL", args.level)

    content_metadata, streams_metadata, minimal_content_compatibility_level = srs_parser.parseJSON(
        args.SRS_file,
        webp_compatible=args.webm
    )
    args.SRS_file.close()

    CONTENT_TITLE = content_metadata["title"]
    print("TITLE:", CONTENT_TITLE)
    if args.level > minimal_content_compatibility_level:
        print("Content compatibility error!")
        print("Minimal content compatibility level is {}.".format(minimal_content_compatibility_level))
        exit(1)

    OUTPUT_FILENAME = "{}.mkv".format(CONTENT_TITLE)

    if args.o is not None:
        OUTPUT_FILENAME = args.o

    print("OUTPUT FILENAME:", OUTPUT_FILENAME)

    commandline = ["mkvmerge", "--title", CONTENT_TITLE, '-o', str(OUTPUT_FILENAME)]

    if streams_metadata[0] is not None:
        vtitle = streams_metadata[0].get_stream_title()
        vlang = streams_metadata[0].get_track_language()
        if vtitle is not None:
            commandline += ['--track-name', "0:{}".format(vtitle)]
        if vlang is not None:
            commandline += ['--language', "0:{}".format(vlang)]
        commandline += [streams_metadata[0].get_compatible_files(args.level)[0]]

    if streams_metadata[1] is not None:
        for stream in streams_metadata[1]:
            astitle = stream.get_stream_title()
            aslang = stream.get_track_language()
            def cl_add_file():
                global commandline
                if astitle is not None:
                    commandline += ['--track-name', "0:{}".format(astitle)]
                if aslang is not None:
                    commandline += ['--language', "0:{}".format(aslang)]
                commandline += [file]
            if args.limit_audio_channels is not None:
                file = stream.get_file(args.limit_audio_channels, args.level)
                if file is not None:
                    cl_add_file()
                    continue
            files = stream.get_compatible_files(args.level)
            for file in files:
                cl_add_file()
                commandline += [file]

    if streams_metadata[2] is not None and not args.webm:
        for stream in streams_metadata[2]:
            stitle = stream.get_stream_title()
            slang = stream.get_track_language()
            if stitle is not None:
                commandline += ['--track-name', "0:{}".format(stitle)]
            if slang is not None:
                commandline += ['--language', "0:{}".format(slang)]
            commandline += [stream.get_compatible_files(args.level)[0]]

    if args.webm:
        commandline += ['--webm']

    subprocess.run(commandline)




