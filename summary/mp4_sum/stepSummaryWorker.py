from summary.config import stepSummaryPromptStart, stepSummaryPromptEnd
from summary.mp4_sum.core import Mp4SummaryWorker
from summary.util.create_llm import get_llm


class stepSummaryWorker(Mp4SummaryWorker):
    def summary(self, text=None, title=None, info=None, PromptStart=stepSummaryPromptStart,
                PromptEnd=stepSummaryPromptEnd):
        """
        视频文本标题,文本附加信息==>chapter摘要
        :param PromptStart: 提示词开始
        :param PromptEnd: 提示词结束
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

        this_prompt = PromptStart + all_info + PromptEnd
        print("开始生成chapter摘要:\n")
        allSummary = llm.invoke(this_prompt).content
        # print(allSummary)
        return allSummary
