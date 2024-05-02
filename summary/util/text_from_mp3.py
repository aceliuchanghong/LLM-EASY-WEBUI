# pip install faster-whisper
from faster_whisper import WhisperModel


def get_whisper_model(model_size_or_path):
    whisperModel = WhisperModel(model_size_or_path=model_size_or_path, device="cuda")
    return whisperModel


def get_whisper_text(whisperModel, audio_path, mode="timeline"):
    transcription = ""
    try:
        segments, info = whisperModel.transcribe(audio_path)
        # 1 以下一般版本
        if mode == "normal":
            transcription_segments = [segment.text for segment in segments]
            # print(transcription_segments)
            transcription = "，".join(transcription_segments)

        # 2 以下加入时间轴版本
        elif mode == "timeline":
            for segment in segments:
                # print("[%.2fs -> %.2fs] %s\n" % (segment.start, segment.end, segment.text))
                transcription += "[%.2fs -> %.2fs] %s\n" % (segment.start, segment.end, segment.text)

        # 3 以下产生字幕格式的版本
        elif mode == "subtitle":
            for i, segment in enumerate(segments, 1):
                start_hours, start_remainder = divmod(segment.start, 3600)
                start_minutes, start_seconds = divmod(start_remainder, 60)
                end_hours, end_remainder = divmod(segment.end, 3600)
                end_minutes, end_seconds = divmod(end_remainder, 60)
                """
                print("%d\n%02d:%02d:%06.3f --> %02d:%02d:%06.3f\n%s\n\n" % (
                    i,
                    start_hours, start_minutes, start_seconds,
                    end_hours, end_minutes, end_seconds,
                    segment.text
                ))
                """
                transcription += "%d\n%02d:%02d:%06.3f --> %02d:%02d:%06.3f\n%s\n\n" % (
                    i,
                    start_hours, start_minutes, start_seconds,
                    end_hours, end_minutes, end_seconds,
                    segment.text
                )
        print("获取视频字幕成功:" + audio_path)
        return transcription
    except Exception as e:
        print("获取视频字幕失败:" + audio_path)
        print(e)
        return transcription


if __name__ == '__main__':
    model_size_or_path = r'C:\Users\lawrence\Documents\large_v3'
    audio_path = r"C:\Users\lawrence\Videos\yunyin.mp4.mp3"
    # normal 一般, timeline 加入时间轴, subtitle 产生字幕格式
    mode = "timeline"

    whisperModel = get_whisper_model(model_size_or_path)
    text = get_whisper_text(whisperModel=whisperModel, audio_path=audio_path, mode=mode)
    print("\n\ntimeline:\n" + text)
