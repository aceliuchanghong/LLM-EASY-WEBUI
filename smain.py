import os
from summary.config import model_size_or_path
from summary.mp4_sum.allSummaryWorker import allSummaryWorker
from summary.mp4_sum.stepSummaryWorker import stepSummaryWorker
import argparse

from summary.text_sum.allSummaryWorker import allTextSummaryWorker
from summary.util.mp3_from_mp4 import get_mp3_from_mp4
from summary.util.text_from_mp3 import get_whisper_model, get_whisper_text

SummaryWorker = {
    "SumMp4Step": stepSummaryWorker,
    "SumMp4All": allSummaryWorker,
    "SumTextAll": allTextSummaryWorker,
}
SummaryMode = {
    "SumMp4Step": "timeline",
    "SumMp4All": "normal",
    "SumTextAll": "normal",
}


def main(summaryType, filePath, fileInfo=None, whisperModel=None):
    """
    插入数据库信息:
    summaryType,filePath,text,fileInfo,sumText,time
    """
    if summaryType not in SummaryWorker:
        print(f"Unsupported summaryType: {summaryType}\n仅支持:SumMp4All,SumMp4Step,SumTextAll")
        return
    if not os.path.exists(filePath):
        print("File doesn't exist in:", filePath)
        return
    if summaryType in ('SumMp4All', 'SumMp4Step'):
        mp3FilePath = get_mp3_from_mp4(filePath)
        text = get_whisper_text(whisperModel=whisperModel, audio_path=mp3FilePath, mode=SummaryMode.get(summaryType))
    else:
        text = None
    print("待总结:" + text)
    Summary = SummaryWorker.get(summaryType)(filePath)
    file_name, file_dir = Summary._get_file_info()
    sumText = Summary.summary(text=text, title=file_name, info=fileInfo)
    print("结果:" + sumText)

    return sumText


if __name__ == "__main__":
    whisperModel = get_whisper_model(model_size_or_path)

    parser = argparse.ArgumentParser(description="various summaryTypes")
    parser.add_argument('--summaryType', required=True, help="总结的类型:SumMp4All,SumMp4Step,SumTextAll")
    parser.add_argument('--filePath', required=True, help="Path of the video file.")
    parser.add_argument('--fileInfo', required=False, help="File describe info.")
    args = parser.parse_args()

    main(args.summaryType, args.filePath, args.fileInfo, whisperModel)
