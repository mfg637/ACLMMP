import json

def parseJSON(fp):
    raw_data = json.load(fp)
    content_metadata = raw_data['content']
    streams_metadata = raw_data['streams']

    video_compatibility_level = -1
    if 'video' in streams_metadata:
        for raw_level in streams_metadata['video']['levels']:
            level = int(raw_level)
            video_compatibility_level = max(level, video_compatibility_level)

    audio_compatibility_level = -1
    if 'audio' in streams_metadata:
        audio_compatibility_level = 5
        for audio_stream in streams_metadata['audio']:
            stream_level = 5
            for channel in audio_stream['channels']:
                channel_level = -1
                for raw_level in audio_stream['channels'][channel]:
                    level = int(raw_level)
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
