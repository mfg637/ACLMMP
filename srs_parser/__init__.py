import json
import enum
import pathlib

from .VideoStream import VideoStream
from .AudioStream import AudioStream
from .SubtitleStream import SubtitleStream
from .ImageFile import ImageFile


class MEDIA_TYPE(enum.Enum):
    IMAGE = 0
    AUDIO = 1
    VIDEO = 2
    VIDEOLOOP = 3


def parseJSON(fp, webp_compatible=False):
    raw_data = json.load(fp)
    content_metadata = raw_data['content']
    video = None
    if 'video' in raw_data['streams']:
        video = VideoStream(raw_data['streams']['video'], webp_compatible)
    audio_streams = None
    if 'audio' in raw_data['streams']:
        audio_streams = [AudioStream(stream, webp_compatible) for stream in raw_data['streams']['audio']]
    subtitle_streams = None
    if 'subtitles' in raw_data['streams']:
        subtitle_streams = [SubtitleStream(stream) for stream in raw_data['streams']['subtitles']]
    image = None
    if 'image' in raw_data['streams']:
        image = ImageFile(raw_data['streams']['image'])
    streams_metadata = (video, audio_streams, subtitle_streams, image)

    video_compatibility_level = -1
    if video is not None:
        for level in video.levels:
            video_compatibility_level = max(level, video_compatibility_level)

    image_compatibility_level = -1
    if image is not None:
        for level in image.levels:
            image_compatibility_level = max(level, image_compatibility_level)

    audio_compatibility_level = -1
    if audio_streams is not None:
        audio_compatibility_level = 5
        for audio_stream in audio_streams:
            stream_level = 5
            for channel in audio_stream.channels:
                channel_level = -1
                for level in audio_stream.channels[channel]:
                    channel_level = max(level, channel_level)
                stream_level = min(channel_level,stream_level)
            audio_compatibility_level = min(stream_level, audio_compatibility_level)

    minimal_content_compatibility_level = -1
    if video_compatibility_level == -1 and audio_compatibility_level != -1:
        minimal_content_compatibility_level = audio_compatibility_level
    elif audio_compatibility_level == -1 and video_compatibility_level != -1:
        minimal_content_compatibility_level = video_compatibility_level
    elif video_compatibility_level == -1 and audio_compatibility_level == -1 and image is not None:
        minimal_content_compatibility_level = image_compatibility_level
    else:
        minimal_content_compatibility_level = min(video_compatibility_level, audio_compatibility_level)
    return content_metadata, streams_metadata, minimal_content_compatibility_level


def get_files_list(srs_path: pathlib.Path, content_metadata, streams_metadata):
    list_files = []
    dir = srs_path.parent

    def get_files_from_levels(levels):
        for level in levels:
            list_files.append(dir.joinpath(levels[level]))

    if "poster-image" in content_metadata:
        get_files_from_levels(content_metadata["poster-image"]['levels'])

    if "convert-image" in content_metadata:
        get_files_from_levels(content_metadata["convert-image"]['levels'])

    if streams_metadata[0] is not None:
        get_files_from_levels(streams_metadata[0].levels)

    if streams_metadata[1] is not None:
        for audio in streams_metadata[1]:
            for channel in audio.channels:
                get_files_from_levels(audio.channels[channel])

    if streams_metadata[2] is not None:
        for subtitle in streams_metadata[2]:
            list_files.append(dir.joinpath(subtitle.file))

    if streams_metadata[3] is not None:
        get_files_from_levels(streams_metadata[3].levels)

    return list_files
