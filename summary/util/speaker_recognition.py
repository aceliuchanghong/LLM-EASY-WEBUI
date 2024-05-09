from speechlib import Transcriptor
from summary.config import model_size_or_path

def get_speaker_whisper_text(modelSize, wav_file, voices_folder, log_folder, language="zh", quantization=False):
    # 有问题
    # quantization = False
    # setting this 'True' may speed up the process but lower the accuracy
    transcriptor = Transcriptor(wav_file, log_folder, language, modelSize, voices_folder, quantization)
    res = transcriptor.transcribe()
    print(res)
    return res


if __name__ == '__main__':
    modelSize = model_size_or_path
    wav_file = r'C:\Users\lawrence\Videos\waijiaobu.mp4.mp3.wav'
    voices_folder = "voices"
    log_folder = "logs"

    get_speaker_whisper_text(modelSize, wav_file, voices_folder, log_folder)
