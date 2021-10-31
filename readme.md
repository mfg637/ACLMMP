# Adaptive Compatibility-Level based Multimedia Multiplexing Protocol

Protocol describes storing media in unmuxed form and muxing it
on demand. Media streams stores in each file separately.
Stream references, and their compatibility levels
describes by "stream references sheet" file.

## Compatibility Levels

0. PC only and software only decoding compatible;
1. PC only with limited hw compatibility;
2. Smart-TV and TV Box device compatibility;
3. Android smartphones compatibility;
4. Wide compatibility.

Compatibility level specifications may be changed by time.
Some specifications changes more often than others.
But now, compatibility-level specks looks like that:

| level | vcodec | bit-depth | pixel format | max framerate | max resolution | acodec |
| ----- | ------ | --------- | ------------ | ------------- | -------------- | ------ |
| 0     | AV1    | 12        | yuv422p12le  | unlimited     | 8k             | opus   |
| 0     | AV1    | 12        | yuv444p12le  | unlimited     | 8k             | opus   |
| 0     | AV1    | 10        | yuv422p10le  | unlimited     | 8k             | opus   |
| 0     | AV1    | 10        | yuv444p10le  | unlimited     | 8k             | opus   |
| 1     | HEVC   | 10        | yuv422p10le  | 60            | 4k             | opus   |
| 1     | HEVC   | 10        | yuv444p10le  | 60            | 4k             | opus   |
| 2     | HEVC   | 10        | yuv420p10le  | 30            | 4k             | opus   |
| 2     | HEVC   | 8         | yuv420p      | 60            | 1080p          | opus   |
| 3     | HEVC   | 8         | yuv420       | 30            | 1080p          | opus   |
| 3, 3w | VP9    | 8         | yuv420       | 30            | 720p          | opus   |
| 4     | AVC    | 8         | yuv420       | 30            | 1080p          | aac    |

### Levels and *w-levels

Level suffix w indicates that video or audio track
compatible to muxing to WEBM container. It helps web server
to select right video or audio track for muxing
(on-demand muxing variant). If WEBM compatibility is not required,
first track with same level has higher priority,
even if it doesn't have *w suffix.

### Forced level

Lover level (with bigger index) can be forced to muxing or playback
by "force-level" stream-metadata value.

Example:

      "video": {
         "title": "VIDEO STREAM TITLE,
         "force-level": 4,
         "levels": {
            "3w": "low quality vp9 transcode.webm", // for webm's
            "4": "original h264 video.mkv" // for mkv's
         }
      }

### compatibility levels for images

| level | format   | bit-depth | pixel format | max resolution |
| ----- | -------- | --------- | ------------ | -------------- |
| 0     | AVIF-AV1 | 12        | yuv422p12le  | -              |
| 0     | AVIF-AV1 | 12        | yuv444p12le  | -              |
| 1     | AVIF-AV1 | 8         | yuv444p      | ≈100 MP        |
| 2     | HEIC     | 10        | yuv420p10le  | 4096x4096      |
| 3     | WEBP     | 8         | yuv420       | 2048x2048      |
| 4     | JPG      | 8         | yuv420       | 1024x1024      |
| 4     | PNG      | 8         | RGB          | 1024x1024      |

## Muxing variants

1. **Online muxing** — client's player muxes streams
   and plays them in real time;
2. **On demand muxing** — server does muxing streams by given
   compatibility level. Client gets already muxed file;
3. **Offline muxing** — same as "on demand muxing",
   but muxed file just stored on client for a while.

## Stream References Sheet file

JSON formatted file, who describes streams,
and provides links marked by compatibility-level.

### Specification

    {"ftype":"CLSRS",
        "content": {
            "title": "CONTENT TITLE",
            "media-type": MEDIA_TYPE,
            /* MEDIA_TYPE(integer) = 
                  IMAGE == 0
                  AUDIO == 1
                  VIDEO == 2
                  VIDEOLOOP == 3
            */
            "poster-image": {// IMAGE_OBJECT
               "levels": {
                  "4": "movie poster.jpg",
               },
               "some metadata": some_value
            }
            "cover-image": {// IMAGE_OBJECT
               "levels": {
                  "4": "album cover.jpg",
               },
               "some metadata": some_value
            },
            "some metadata": some_value
        },
        "streams":{
            "video": {
                "title": "VIDEO STREAM TITLE (non-required),
                "some metadata": some_value,
                "levels": {
                     /* "LEVEL_ID(integer)[w]": "FILE_URL(string) */"
                    "0": "master quality video.mkv",
                    "1": "high quality file.mkv",
                    "2": "medium quality file.mkv",
                    "3": "low quality file.mkv"
                    "3w": "low quality vp9 video.mkv"
                }
            },
            "audio":[
                {
                    "title": "original soundtrack",
                    "language": "eng",
                    "channels": {
                        /* "CHANNELS_COUNT(integer)": {LEVELS_LIST_OBJECT}
                        "2": {
                           /* "LEVEL_ID(integer)[w]": "FILE_URL(string) */"
                           "3w": "01 128kbps.opus",
                           "4": "01 128kbps aac.m4a"
                        },
                        "6": {
                            "3": "01 384kbps.opus"
                        }
                    }
                },
                {
                    "title": "some language DUB",
                    "language": "und",
                    "channels": {
                        "2": {
                            "3w": "02 128kbps.opus",
                            "4": "02 128kbps aac.m4a"
                        },
                        "6": {
                            "4": "02 384kbps.ac3"
                        }
                    }
                }
            ],
            "subtitles":[
                {
                    "title": "some language sub"
                    "language": "und",
                    "file": "sub.srt"
                },
                {
                    "title": "orig sub"
                    "language": "eng",
                    "file": "orig.ass"
                }
            ],
            "image":{// IMAGE_OBJECT
               "levels": {
                  "1": "image.avif"
                  "3": "preview.webp",
                  "4": "thumbnail.jpg",
               },
               "some metadata": some_value
            }
        }
    }
