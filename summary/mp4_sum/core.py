from summary.worker.Worker import MediaSummaryWorker


class Mp4SummaryWorker(MediaSummaryWorker):
    def __init__(self, file_path):
        super().__init__(file_path)

    def summary(self, *args, **kwargs):
        # Implementation specific to MP4 processing
        pass
