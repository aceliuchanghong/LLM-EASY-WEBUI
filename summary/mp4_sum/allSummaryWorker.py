from summary.config import model_size_or_path, allSummaryPromptStart, allSummaryPromptEnd
from summary.mp4_sum.core import Mp4SummaryWorker
from summary.util.create_llm import get_llm
from summary.util.text_from_mp3 import get_whisper_model, get_whisper_text


class allSummaryWorker(Mp4SummaryWorker):
    def summary(self, mode="normal", text=None, title=None, info=None):
        """
        视频文本标题,文本附加信息==>总体摘要
        :param mode: 文本生成的形式
        :param text: 文本
        :param title: 文本标题
        :param info: 文本附加信息
        """
        mp3_file_path = self._get_mp3_from_mp4()
        whisperModel = get_whisper_model(model_size_or_path)
        llm = get_llm()

        text = get_whisper_text(whisperModel=whisperModel, audio_path=mp3_file_path, mode=mode)

        all_info = text
        if title:
            all_info += "\n视频标题:" + title
        if info:
            all_info += "\n视频备注:" + info

        this_prompt = allSummaryPromptStart + all_info + allSummaryPromptEnd
        print("开始生成总体摘要:")
        allSummary = llm.invoke(this_prompt).content
        # print(llm.invoke(this_prompt))
        print(allSummary)
        return allSummary


if __name__ == '__main__':
    mp4_path = r"C:\Users\lawrence\Videos\yunyin.mp4"
    allSum = allSummaryWorker(mp4_path)
    ans = allSum.summary(title="说剑", info="中国古文")
    print("结果:" + ans)
