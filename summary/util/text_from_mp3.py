# pip install faster-whisper
from faster_whisper import WhisperModel

model_size_or_path = r'C:\Users\lawrence\Documents\large_v3'
audio_path = r"C:\Users\lawrence\Videos\yunyin.mp4.mp3"
# normal 一般, timeline 加入时间轴, subtitle 产生字幕格式
mode = "timeline"
transcription = ""

model = WhisperModel(model_size_or_path=model_size_or_path, device="cuda")

segments, info = model.transcribe(audio_path)

# 1 以下一般版本
if mode == "normal":
    transcription_segments = [segment.text for segment in segments]
    transcription = "，".join(transcription_segments)

# 2 以下加入时间轴版本
elif mode == "timeline":
    for segment in segments:
        transcription += "[%.2fs -> %.2fs] %s\n" % (segment.start, segment.end, segment.text)

# 3 以下产生字幕格式的版本
elif mode == "subtitle":
    for i, segment in enumerate(segments, 1):
        start_hours, start_remainder = divmod(segment.start, 3600)
        start_minutes, start_seconds = divmod(start_remainder, 60)
        end_hours, end_remainder = divmod(segment.end, 3600)
        end_minutes, end_seconds = divmod(end_remainder, 60)
        transcription += "%d\n%02d:%02d:%06.3f --> %02d:%02d:%06.3f\n%s\n\n" % (
            i,
            start_hours, start_minutes, start_seconds,
            end_hours, end_minutes, end_seconds,
            segment.text
        )

print(transcription)
