import os
from summary.config import (model_size_or_path,
                            table_select_sum_sql,
                            table_del_url_sql,
                            table_add_sql,
                            create_table_sql,
                            table_select_text_sql)
from summary.mp4_sum.allSummaryWorker import allSummaryWorker
from summary.mp4_sum.stepSummaryWorker import stepSummaryWorker
import argparse
from datetime import datetime
from summary.text_sum.allSummaryWorker import allTextSummaryWorker
from summary.util.check_db import check, excute_sqlite_sql
from summary.util.mp3_from_mp4 import is_audio_file, get_mp3_from_video
from summary.util.text_from_mp3 import get_whisper_model, get_whisper_text

SummaryWorker = {
    "SumMp4Step": stepSummaryWorker,
    "SumMp4All": allSummaryWorker,
    "SumTextAll": allTextSummaryWorker,
}
SummaryMode = {
    "SumMp4Step": "timeline",
    "SumMp4All": "timeline",
    "SumTextAll": "normal",
}


def main(summaryType, filePath, fileInfo=None, whisperModel=None, reRun=False):
    """
    插入数据库信息:
    summaryType,filePath,text,fileInfo,sumText,time
    """
    # 数据库校验
    if not reRun:
        if check(summaryType, filePath) != 0:
            print(f"The {summaryType}:{filePath} have already been summaried")
            print("待总结:\n" + excute_sqlite_sql(table_select_text_sql, (summaryType, filePath), False)[0][0])
            print("结果:\n" + excute_sqlite_sql(table_select_sum_sql, (summaryType, filePath), False)[0][0])
            return excute_sqlite_sql(table_select_text_sql, (summaryType, filePath), False)[0][0], \
                excute_sqlite_sql(table_select_sum_sql, (summaryType, filePath), False)[0][0]
    if reRun:
        excute_sqlite_sql(table_del_url_sql, (summaryType, filePath), False)
    # 参数校验
    if summaryType not in SummaryWorker:
        print(f"Unsupported summaryType: {summaryType}\n仅支持:SumMp4All,SumMp4Step,SumTextAll")
        return "总结方法有误", "总结失败"
    if not os.path.exists(filePath):
        print("File doesn't exist in:", filePath)
        return filePath + "文件不存在", "总结失败"

    # 开始执行
    if summaryType in ('SumMp4All', 'SumMp4Step'):
        # print(is_audio_file(filePath))
        if is_audio_file(filePath):
            mp3FilePath = filePath
        else:
            mp3FilePath = get_mp3_from_video(filePath)
        text = get_whisper_text(whisperModel=whisperModel, audio_path=mp3FilePath, mode=SummaryMode.get(summaryType))
    else:
        text = None
    print("待总结:\n" + text)
    Summary = SummaryWorker.get(summaryType)(filePath)
    file_name, file_dir = Summary._get_file_info()
    if len(text) > 4000:
        print("待处理")
    text_go_sum = text[:4000]
    sumText = Summary.summary(text=text_go_sum, title=file_name, info=fileInfo)
    print("结果:\n" + sumText)

    # 存储进入数据库
    excute_sqlite_sql(
        table_add_sql,
        (summaryType, filePath, text, fileInfo, sumText, str(datetime.now().strftime('%Y%m%d')), "remark"),
        False)
    return text, sumText


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
