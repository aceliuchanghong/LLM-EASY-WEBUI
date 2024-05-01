from mp4_utils.converters.mp4_to_mp3 import MP4ToMP3Converter

from summary.worker.Worker import MediaSummaryWorker


class Mp4SummaryWorker(MediaSummaryWorker):
    def __init__(self, file_path):
        super().__init__(file_path)

    def summary(self, *args, **kwargs):
        # Implementation specific to MP4 processing
        pass

    def _get_mp3_from_mp4(self):
        self._validate_path(self.file_path)
        converter = MP4ToMP3Converter(self.file_path)
        file_name, file_dir = self._get_file_info()
        print(file_name, file_dir)
        result = file_dir + "/" + file_name + ".mp3"
        converter.process(result)
        return result
