from summary.mp4_sum.core import Mp4SummaryWorker


class stepSummaryWorker(Mp4SummaryWorker):
    def summary(self, title=None, info=None, mode="timeline"):
        """
        视频文本标题,文本附加信息==>步骤摘要
        :param mode: 文本生成的形式
        :param title: 文本标题
        :param info: 文本附加信息
        :return: str: 步骤摘要
        """
        print("start")
