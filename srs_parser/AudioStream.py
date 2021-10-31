from .Stream import Stream


class AudioStream(Stream):
    def __init__(self, json_data, webm_compatible=False):
        super().__init__()
        self.channels = dict()
        for raw_channel in json_data['channels']:
            channel = int(raw_channel)
            levels = dict()
            for raw_level in json_data['channels'][raw_channel]:
                self.level_parse(
                    raw_level,
                    webm_compatible,
                    input_value=json_data['channels'][raw_channel],
                    output=levels)
            self.channels[channel] = levels
        self.tags = dict()
        for tag in json_data:
            if tag != 'channels':
                self.tags[tag] = json_data[tag]

    def get_compatible_files(self, target_level: int) -> tuple:
        files = []
        for channel in self.channels:
            for current_level in range(target_level, 5):
                if current_level in self.channels[channel]:
                    files.append(self.channels[channel][current_level])
                    break
        return tuple(files)

    def get_file(self, max_channels, target_level):
        for channel in range(max_channels, 0, -1):
            if channel in self.channels:
                for current_level in range(target_level, 5):
                    if current_level in self.channels[channel]:
                        return self.channels[channel][current_level]
        return None

