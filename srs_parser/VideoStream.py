from .Stream import Stream


class VideoStream(Stream):
    def __init__(self, json_data, webm_compatible=False):
        self.levels = dict()
        for raw_level in json_data['levels']:
            self.level_parse(raw_level, webm_compatible, input_value=json_data['levels'], output=self.levels)
        self.tags = dict()
        for tag in json_data:
            if tag != 'levels':
                self.tags[tag] = json_data[tag]

    def get_compatible_files(self, target_level: int) -> tuple:
        if "force-level" in self.tags and self.tags["force-level"] >= target_level:
            if self.tags["force-level"] in self.levels:
                return self.levels[self.tags["force-level"]],
        for current_level in range(target_level, 5):
            if current_level in self.levels:
                return self.levels[current_level],
        raise Exception("Compatible level not founded")


