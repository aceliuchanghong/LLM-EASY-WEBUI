from summary.worker.Worker import MediaSummaryWorker


class TextSummaryWorker(MediaSummaryWorker):
    def __init__(self, file_path):
        super().__init__(file_path)

    def summary(self, *args, **kwargs):
        # Implementation specific file summary processing
        pass
