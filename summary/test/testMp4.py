from summary.mp4_sum.core import Mp4SummaryWorker


def main() -> Mp4SummaryWorker:
    path1 = r'C:\Users\lawrence\Videos\yunyin.mp4'
    path2 = '../t'
    mp4SummaryWorker = Mp4SummaryWorker(path1)
    file_name, file_dir = mp4SummaryWorker._get_file_info()
    print(file_name, file_dir)
    # mp4SummaryWorker._validate_path(path2)
    return mp4SummaryWorker


if __name__ == '__main__':
    print(main()._get_mp3_from_mp4())
