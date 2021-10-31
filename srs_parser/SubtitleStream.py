from .Stream import Stream


class SubtitleStream(Stream):
    def __init__(self, json_data):
        super().__init__()
        self.file = json_data['file']
        self.tags = dict()
        for tag in json_data:
            if tag != 'file':
                self.tags[tag] = json_data[tag]

    def get_compatible_files(self, target_level: int) -> tuple:
        return self.file,
