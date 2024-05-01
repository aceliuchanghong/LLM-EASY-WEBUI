from abc import ABC, abstractmethod
import os


class MediaSummaryWorker(ABC):
    """
    Abstract base class for file handling.
    mp4,ppt,pdf,doc,docx
    """

    def __init__(self, file_path):
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        self.file_path = file_path

    @abstractmethod
    def summary(self, *args, **kwargs):
        """
        Process summary file.
        """
        pass

    def _validate_path(self, path):
        """
        Validate the path. If the path is a directory, create it if it doesn't exist.
        If it's a file path and the directory does not exist, create it.
        """
        if os.path.isdir(path) or not os.path.splitext(path)[1]:
            output_dir = path
        else:
            output_dir = os.path.dirname(path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return path

    def _get_file_info(self):
        file_name = os.path.basename(self.file_path)
        file_dir = os.path.dirname(self.file_path)
        return file_name, file_dir
