#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import srs_parser

if __name__ == "__main__":
    fp = open(sys.argv[1], "r")
    content_metadata, streams_metadata, minimal_content_compatibility_level = srs_parser.parseJSON(fp)
    fp.close()

    print("CONTENT METADATA:")
    for key in content_metadata:
        print("    {}:".format(key), content_metadata[key])
    print()

    if streams_metadata[0] is not None:
        print("VIDEO STREAMS METADATA:")
        for key in streams_metadata[0].tags:
            print("    {}:".format(key), streams_metadata[0].tags[key])
        print()

    if streams_metadata[1] is not None:
        print("AUDIO STREAMS METADATA:")
        i = 0
        for audio_stream in streams_metadata[1]:
            print("    AUDIO STREAM #{}".format(i))
            i += 1
            available_channels = ""
            for channel in audio_stream.channels:
                if len(available_channels):
                    available_channels += ", {}".format(channel)
                else:
                    available_channels = str(channel)
            print("        AVAILABLE CHANNELS: {}".format(available_channels))
            for key in audio_stream.tags:
                print("        {}:".format(key), audio_stream.tags[key])
        print()

    if streams_metadata[2] is not None:
        print("SUBTITLE STREAMS METADATA:")
        i = 0
        for subtitle_stream in streams_metadata[2]:
            print("    SUBTITLE STREAM #{}".format(i))
            i += 1
            for key in subtitle_stream.tags:
                print("        {}:".format(key), subtitle_stream.tags[key])
        print()

    print("MINIMAL CONTENT COMPATIBILITY LEVEL:", minimal_content_compatibility_level)
