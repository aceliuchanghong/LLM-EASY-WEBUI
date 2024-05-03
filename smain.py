from summary.mp4_sum.allSummaryWorker import allSummaryWorker
from summary.mp4_sum.stepSummaryWorker import stepSummaryWorker
import argparse

SummaryWorker = {
    "SumMp4Step": stepSummaryWorker,
    "SumMp4All": allSummaryWorker,
}


def main(summaryType, filePath):
    if summaryType not in SummaryWorker:
        print(f"Unsupported summaryType: {summaryType}\n仅支持:SumMp4All,SumMp4Step")
        return
    Summary = SummaryWorker.get(summaryType)(filePath)
    if not Summary._is_exists():
        print("视频不存在,退出程序")
        return
    Summary.summary()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload videos to various platforms.")

    parser.add_argument('--summaryType', required=True, help="总结的类型:SumMp4All,SumMp4Step")
    parser.add_argument('--filePath', required=True, help="Path of the video file.")
    args = parser.parse_args()

    main(args.summaryType, args.filePath)
