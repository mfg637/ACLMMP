import sys

import srs_parser
fp = open(sys.argv[1], "r")
content_metadata, streams_metadata, minimal_content_compatibility_level = srs_parser.parseJSON(fp)
fp.close()

print("CONTENT METADATA:")
for key in content_metadata:
    print("    {}:".format(key), content_metadata[key])
print()

if 'video' in streams_metadata:
    print("VIDEO STREAMS METADATA:")
    for key in streams_metadata['video']:
        if key != "levels":
            print("    {}:".format(key), streams_metadata['video'][key])
    print()

if 'audio' in streams_metadata:
    print("AUDIO STREAMS METADATA:")
    i = 0
    for audio_stream in streams_metadata['audio']:
        print("    AUDIO STREAM #{}".format(i))
        i += 1
        for key in audio_stream:
            if key == "channels":
                available_channels = ""
                for channel in audio_stream["channels"]:
                    if len(available_channels):
                        available_channels += ", {}".format(channel)
                    else:
                        available_channels = channel
                print("        AVAILABLE CHANNELS: {}".format(available_channels))
            else:
                print("        {}:".format(key), audio_stream[key])
    print()

if 'subtitles' in streams_metadata:
    print("SUBTITLE STREAMS METADATA:")
    i = 0
    for subtitle_stream in streams_metadata['subtitles']:
        print("    SUBTITLE STREAM #{}".format(i))
        i += 1
        for key in subtitle_stream:
            print("        {}:".format(key), subtitle_stream[key])
    print()

print("MINIMAL CONTENT COMPATIBILITY LEVEL:", minimal_content_compatibility_level)
