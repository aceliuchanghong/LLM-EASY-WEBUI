import os
from summary.config import model_size_or_path, table_select_sum_sql, table_del_url_sql, table_add_sql, create_table_sql
from summary.mp4_sum.allSummaryWorker import allSummaryWorker
from summary.mp4_sum.stepSummaryWorker import stepSummaryWorker
import argparse
from datetime import datetime
from summary.text_sum.allSummaryWorker import allTextSummaryWorker
from summary.util.check_db import check, excute_sqlite_sql
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


def main(summaryType, filePath, fileInfo=None, whisperModel=None, reRun=False):
    """
    插入数据库信息:
    summaryType,filePath,text,fileInfo,sumText,time
    """
    if not reRun:
        if check(summaryType, filePath) != 0:
            print(f"The {summaryType}:{filePath} have already been summaried")
            return excute_sqlite_sql(table_select_sum_sql(summaryType, filePath), False)
    if reRun:
        excute_sqlite_sql(table_del_url_sql(summaryType, filePath), False)
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
    print("待总结:\n" + text)
    Summary = SummaryWorker.get(summaryType)(filePath)
    file_name, file_dir = Summary._get_file_info()
    sumText = Summary.summary(text=text, title=file_name, info=fileInfo)
    print("结果:\n" + sumText)
    excute_sqlite_sql(
        table_add_sql(summaryType, filePath, text, fileInfo, sumText, str(datetime.now().strftime('%Y%m%d')), "remark"),
        False)
    return sumText


if __name__ == "__main__":
    whisperModel = get_whisper_model(model_size_or_path)
    excute_sqlite_sql(create_table_sql)

    parser = argparse.ArgumentParser(description="various summaryTypes")
    parser.add_argument('--summaryType', required=True, help="总结的类型:SumMp4All,SumMp4Step,SumTextAll")
    parser.add_argument('--filePath', required=True, help="Path of the video file.")
    parser.add_argument('--fileInfo', required=False, help="File describe info.")
    parser.add_argument('--reRun', required=False, action='store_true'
                        , help="是否删除数据库该数据然后重跑", default=False)
    args = parser.parse_args()

    main(args.summaryType, args.filePath, args.fileInfo, whisperModel, args.reRun)
