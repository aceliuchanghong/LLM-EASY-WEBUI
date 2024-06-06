from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from typing import List
import os
from funasr import AutoModel
import re
import uvicorn

app = FastAPI()

# 提前加载模型
model = AutoModel(model='/mnt/data/speech_paraformer-large-vad-punc-spk_asr_nat-zh-cn',
                  vad_model='/mnt/data/speech_fsmn_vad_zh-cn-16k-common-pytorch',
                  punc_model='/mnt/data/punc_ct-transformer_cn-en-common-vocab471067-large',
                  spk_model="/mnt/data/speech_campplus_sv_zh-cn_16k-common")


def process_sentences(res, mode='normal'):
    result = []
    if mode == 'normal':
        current_speaker = None
        current_sentence = None
        for sentence_info in res[0]['sentence_info']:
            spe = sentence_info['spk']
            text = sentence_info['text']
            if current_speaker is None or spe != current_speaker:
                if current_sentence:
                    result.append((current_speaker, current_sentence))
                current_speaker = spe
                current_sentence = text
            else:
                current_sentence += text
        if current_sentence:
            result.append((current_speaker, current_sentence))
        return result
    elif mode == 'timeline':
        # 初始化变量
        current_spk = None
        current_sentence = None
        for sentence_info in res[0]['sentence_info']:
            # 检查当前说话人是否与上一句不同
            if current_spk != sentence_info['spk']:
                # 如果当前句子不为None，则将其添加到结果列表中
                if current_sentence:
                    result.append(current_sentence)
                # 重置当前说话人和当前句子
                current_spk = sentence_info['spk']
                current_sentence = {
                    'text': sentence_info['text'],
                    'start': sentence_info['start'],
                    'end': sentence_info['end'],
                    'spk': sentence_info['spk']
                }
            else:
                # 更新当前句子的结束时间
                current_sentence['end'] = sentence_info['end']
                # 将当前句子的文本追加到当前句子文本后面
                current_sentence['text'] += sentence_info['text']
        # 确保最后一个句子被添加到结果列表中
        if current_sentence:
            result.append(current_sentence)
        return result
    else:
        return ["Unsupported " + mode + " provide."]


def format_timestamp(timestamp):
    # 将时间戳转换为整数分钟和秒
    minutes, seconds = divmod(timestamp / 1000, 60)
    # 格式化为字符串，保留两位小数
    formatted_time = f"{minutes * 60 + seconds:05.2f}s"
    return formatted_time


@app.post("/video")
async def process_video(files: List[UploadFile] = File(...),
                        initial_prompt: str = Form("会议"),
                        mode: str = Form("normal")
                        ):
    print(f'files:{files}, initial_prompt: {initial_prompt}, mode: {mode}')
    information = []
    for file in files:
        # 保存音视频文件
        file_path = os.path.join('/mnt/data/video', file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # 进行识别操作
        res = model.generate(input=file_path, batch_size_s=1000, hotword=initial_prompt)

        chinese_punctuation_pattern = re.compile(r'[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+')
        # 调用递归函数开始处理
        processed_sentences = process_sentences(res, mode)
        # 打印结果列表，并删除除了最后一句的中文标点
        if mode == 'normal':
            for speaker, sentence in processed_sentences:
                cleaned_sentence = chinese_punctuation_pattern.sub('', sentence)
                info = 'spk' + str(speaker) + ":" + cleaned_sentence
                print(info)
                information.append(info)
        elif mode == 'timeline':
            for _ in processed_sentences:
                speaker = _['spk']
                cleaned_sentence = chinese_punctuation_pattern.sub('', _['text'])
                start = format_timestamp(_['start'])
                end = format_timestamp(_['end'])
                info = 'spk' + str(speaker) + ":[" + start + ' -> ' + end + '] ' + cleaned_sentence
                print(info)
                information.append(info)
        # 将结果保存到文件
        result_file_path = os.path.join('/mnt/data/result', f"{os.path.splitext(file.filename)[0]}.txt")
        with open(result_file_path, 'w') as f:
            for item in res:
                # 如果结果是字典对象，则转换为字符串
                if isinstance(item, dict):
                    item = str(item)
                f.write(str(item) + '\n')

        # 删除音视频文件
        os.remove(file_path)

    return {
        "message": "Processing complete",
        "information": information
    }


if __name__ == "__main__":
    """
    nohup python main.py >smain.log &
    """
    uvicorn.run(app, host="0.0.0.0", port=8083)
