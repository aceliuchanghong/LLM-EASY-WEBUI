import os
from summary.config import (model_size_or_path,
                            table_select_sum_sql,
                            table_del_url_sql,
                            table_add_sql,
                            create_table_sql,
                            table_select_text_sql,
                            stepSummaryConnStart,
                            stepSummaryConnEnd,
                            allSummaryConnStart,
                            allSummaryConnEnd,
                            segment_length,
                            textAllSummaryConnEnd,
                            textAllSummaryConnStart)
from summary.mp4_sum.allSummaryWorker import allSummaryWorker
from summary.mp4_sum.stepSummaryWorker import stepSummaryWorker
import argparse
from datetime import datetime
from summary.text_sum.textAllSummaryWorker import allTextSummaryWorker
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
    "SumTextAll": "timeline",
}
SummaryPrompt = {
    "SumMp4Step": [stepSummaryConnStart, stepSummaryConnEnd],
    "SumMp4All": [allSummaryConnStart, allSummaryConnEnd],
    "SumTextAll": [textAllSummaryConnStart, textAllSummaryConnEnd],
}


def crack_long_text(text, Summary, file_name, fileInfo):
    sumText = ""
    total_segments = (len(text) + segment_length - 1) // segment_length  # 计算总段数

    # 分段处理
    start_index = 0
    for i in range(0, total_segments):
        segment_index = i + 1  # 计算当前段的索引
        print(f"正在处理第{segment_index}分段, 共{total_segments}段\n")

        # 确保分割点在segment_length之前
        segment_text = text[start_index:start_index + segment_length].strip()

        # 找到最近的换行符位置
        newline_pos = text.find('\n', start_index + segment_length, start_index + segment_length + segment_length)
        if newline_pos != -1:
            # 如果找到了换行符，确保分割点在换行符之前
            segment_text = text[start_index:newline_pos].strip()
            start_index = newline_pos + 1  # 更新下一个分段的起始点
        else:
            # 如果没有找到换行符，确保分割点在segment_length之前
            start_index += segment_length  # 更新下一个分段的起始点

        # print("dealing:", segment_text)
        segment_summary = Summary.summary(text=segment_text, title=file_name, info=fileInfo)
        sumText += segment_summary

    return sumText


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
    if summaryType in ('SumMp4All', 'SumMp4Step', 'SumTextAll'):
        if is_audio_file(filePath):
            mp3FilePath = filePath
        else:
            mp3FilePath = get_mp3_from_video(filePath)
        text = get_whisper_text(whisperModel=whisperModel, audio_path=mp3FilePath, initial_prompt=fileInfo,
                                mode=SummaryMode.get(summaryType))
    else:
        text = None
    print("待总结:\n" + text)
    Summary = SummaryWorker.get(summaryType)(filePath)
    file_name, file_dir = Summary._get_file_info()

    sumText = crack_long_text(text, Summary, file_name, fileInfo)

    if summaryType in ('SumTextAll', 'SumMp4All'):
        print("开始合并摘要:\n", sumText, "\n可能需要等待一下")
        sumTextAns = Summary.summary(text=sumText,
                                     title=file_name,
                                     info=fileInfo,
                                     PromptStart=SummaryPrompt[summaryType][0],
                                     PromptEnd=SummaryPrompt[summaryType][1])
    else:
        sumTextAns = sumText
    remark = "remark"
    print("结果:\n" + sumTextAns)

    # 存储进入数据库
    excute_sqlite_sql(
        table_add_sql,
        (summaryType, filePath, text, fileInfo, sumTextAns, str(datetime.now().strftime('%Y%m%d')), remark),
        False)
    return text, sumTextAns


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
