from . import VideoStream

class ImageFile(VideoStream):
    def __init__(self, json_data):
        super().__init__(json_data)

