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
