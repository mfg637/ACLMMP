import json

from .VideoStream import VideoStream
from .AudioStream import AudioStream
from .SubtitleStream import SubtitleStream


def parseJSON(fp):
    raw_data = json.load(fp)
    content_metadata = raw_data['content']
    video = None
    if 'video' in raw_data['streams']:
        video = VideoStream(raw_data['streams']['video'])
    audio_streams = None
    if 'audio' in raw_data['streams']:
        audio_streams = [AudioStream(stream) for stream in raw_data['streams']['audio']]
    subtitle_streams = None
    if 'subtitles' in raw_data['streams']:
        subtitle_streams = [SubtitleStream(stream) for stream in raw_data['streams']['subtitles']]
    streams_metadata = (video, audio_streams, subtitle_streams)

    video_compatibility_level = -1
    if video is not None:
        for level in video.levels:
            video_compatibility_level = max(level, video_compatibility_level)

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
    if video_compatibility_level == -1:
        minimal_content_compatibility_level = audio_compatibility_level
    elif audio_compatibility_level == -1:
        minimal_content_compatibility_level = video_compatibility_level
    else:
        minimal_content_compatibility_level = min(video_compatibility_level, audio_compatibility_level)
    return content_metadata, streams_metadata, minimal_content_compatibility_level
