import abc


class Stream(abc.ABC):
    @abc.abstractmethod
    def get_compatible_files(self, target_level: int) -> tuple:
        pass

    def get_stream_title(self):
        if 'title' in self.tags:
            return self.tags['title']
        return None

    def get_track_language(self):
        if 'language' in self.tags:
            return self.tags['language']
        return None

    @staticmethod
    def level_detect_default(raw_level):
        level = -1
        if 'w' in raw_level:
            level = int(raw_level[:-1])
        else:
            level = int(raw_level)
        return level

    @staticmethod
    def level_detect_webm(raw_level):
        level = -1
        if 'w' in raw_level:
            level = int(raw_level[:-1])
        else:
            return None
        return level

    def level_parse(self, raw_level, webm_compatible, input_value, output):
        level = None
        if webm_compatible:
            level = self.level_detect_webm(raw_level)
        else:
            level = self.level_detect_default(raw_level)
        if level is not None and level not in output:
            output[level] = input_value[raw_level]
