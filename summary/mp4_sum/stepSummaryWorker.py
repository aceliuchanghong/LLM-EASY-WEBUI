from summary.config import stepSummaryPromptStart, stepSummaryPromptEnd
from summary.mp4_sum.core import Mp4SummaryWorker
from summary.util.create_llm import get_llm


class stepSummaryWorker(Mp4SummaryWorker):
    def summary(self, text=None, title=None, info=None):
        """
        视频文本标题,文本附加信息==>chapter摘要
        :param text: 文本
        :param title: 文本标题
        :param info: 文本附加信息
        """
        llm = get_llm()

        all_info = text
        if title:
            all_info += "\n视频标题:" + title
        if info:
            all_info += "\n视频关键字备注:" + info

        this_prompt = stepSummaryPromptStart + all_info + stepSummaryPromptEnd
        print("开始生成chapter摘要:")
        allSummary = llm.invoke(this_prompt).content
        return allSummary
