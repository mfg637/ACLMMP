from .Stream import Stream


class VideoStream(Stream):
    def __init__(self, json_data):
        self.levels = dict()
        for raw_level in json_data['levels']:
            level = int(raw_level)
            self.levels[level] = json_data['levels'][raw_level]
        self.tags = dict()
        for tag in json_data:
            if tag != 'levels':
                self.tags[tag] = json_data[tag]

    def get_compatible_files(self, target_level: int) -> tuple:
        for current_level in range(target_level, 5):
            if current_level in self.levels:
                return self.levels[current_level],
        raise Exception("Compatible level not founded")


