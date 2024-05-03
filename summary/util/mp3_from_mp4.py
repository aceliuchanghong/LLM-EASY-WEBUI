import os
from mp4_utils.converters.mp4_to_mp3 import MP4ToMP3Converter


def get_file_info(file_path):
    file_name = os.path.basename(file_path)
    file_dir = os.path.dirname(file_path)
    return file_name, file_dir


def get_mp3_from_mp4(file_path):
    converter = MP4ToMP3Converter(file_path)
    file_name, file_dir = get_file_info(file_path)
    result = file_dir + "/" + file_name + ".mp3"
    try:
        converter.process(result)
        print("视频转音频成功:" + result)
        return result
    except Exception as e:
        print("视频转音频失败:" + file_path)
        print(e)
        return None
