from mp4_utils.converters.mp4_to_mp3 import MP4ToMP3Converter
from moviepy.editor import *
import mimetypes


def get_file_info(file_path):
    file_name = os.path.basename(file_path)
    file_dir = os.path.dirname(file_path)
    return file_name, file_dir


def get_file_extension(file_path):
    # 使用os.path模块的splitext方法获取文件后缀
    _, file_extension = os.path.splitext(file_path)
    return file_extension


def is_audio_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith('audio')


def is_video_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith('video')


def is_media_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith(('audio', 'video'))


def get_media_files(file_default_path):
    media_files = []
    for root, dirs, files in os.walk(file_default_path):
        for f in files:
            file_path = os.path.join(root, f)
            if is_media_file(file_path):
                media_files.append(os.path.relpath(file_path, file_default_path))
    return media_files


def get_mp3_from_mp4_2(file_path):
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


def get_mp3_from_video(file_path, trans_type='mp3'):
    file_name, file_dir = get_file_info(file_path)
    result = file_dir + "/" + file_name + "." + trans_type

    video = VideoFileClip(file_path)
    audio = video.audio
    audio.write_audiofile(result)
    try:
        audio.write_audiofile(result)
        print("视频转音频成功:" + result)
        return result
    except Exception as e:
        print("视频转音频失败:" + file_path)
        print(e)
        return None


def get_mp3_from_audio(file_path, trans_type='mp3'):
    file_name, file_dir = get_file_info(file_path)
    result = file_dir + "/" + file_name + "." + trans_type

    audio = AudioFileClip(file_path)
    audio.write_audiofile(result)
    try:
        audio.write_audiofile(result)
        print("音频格式转化成功:" + result)
        return result
    except Exception as e:
        print("音频格式转化失败:" + file_path)
        print(e)
        return None


if __name__ == '__main__':
    file = r'C:\Users\lawrence\Videos\waijiaobu.mp4.mp3'
    wav_file = get_mp3_from_audio(file, 'wav')
