from summary.config import allSummaryPromptStart, allSummaryPromptEnd
from summary.mp4_sum.core import Mp4SummaryWorker
from summary.util.create_llm import get_llm


class allSummaryWorker(Mp4SummaryWorker):
    def summary(self, text=None, title=None, info=None):
        """
        视频文本标题,文本附加信息==>总体摘要
        :param text: 文本
        :param title: 文本标题
        :param info: 文本附加信息
        """
        llm = get_llm()

        all_info = text
        if title:
            all_info += "\n视频标题:" + title
        if info:
            all_info += "\n视频备注:" + info

        this_prompt = allSummaryPromptStart + all_info + allSummaryPromptEnd
        print("开始生成总体摘要:")
        allSummary = llm.invoke(this_prompt).content
        return allSummary


if __name__ == '__main__':
    mp4_path = r"C:\Users\lawrence\Videos\yunyin.mp4"
    allSum = allSummaryWorker(mp4_path)
    text = """
    愿起一剑杀万劫，无情换作有情天，天子之剑，以宴席时成为风，席代为恶，敬畏为极，周颂为禅，含畏为家，包以四夷，国以四十，绕以渤海，带以长山，智以武行，论以行德，开以阴阳，识以春夏，行以秋冬，此剑直之无前，举之无上，按之无下
，应之无旁，上结浮云，下绝地际，此剑以用，荒诸侯，天下福矣，此天子之剑也，诸侯之剑，以知勇士为风，以青年，识为恶，以贤良事为极，以周颂事为禅，以豪杰事为家，此剑直之亦无前，止之亦无上，按之亦无下，应之亦无旁，上法言天，以顺三光 
，下法方地，以顺四时，综合名义，以安四乡，此剑以用，如雷霆之战也，四方之阴，斧之类，无不兵符，而听从之命折翼，此诸侯之剑也
    """
    ans = allSum.summary(text=text, title="说剑", info="中国古文")
    print("结果:" + ans)
