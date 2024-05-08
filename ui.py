import gradio as gr
import os
from smain import main
from summary.util.text_from_mp3 import get_whisper_model
from summary.config import (model_size_or_path,
                            file_default_path)
from fastapi import FastAPI

app = FastAPI()
SummaryType = {
    "总体摘要": "SumMp4All",
    "章节摘要": "SumMp4Step",
}

reRunType = {
    "是": True,
    "否": False,
}


def doIt(summary_type, file_Path, file_get_type='upload', file_Info=None, re_run=False):
    if file_get_type == 'choose':
        file_Path = file_default_path + "/" + file_Path
    if file_Path.endswith('.mp3'):
        print('mp3', file_Path)
    else:
        print('mp4', file_Path)

    summaryType = SummaryType[summary_type]
    fileInfo = file_Info
    reRun = reRunType[re_run]
    print(summaryType, fileInfo, reRun)
    whisperModel = get_whisper_model(model_size_or_path)

    return main(summaryType, file_Path, fileInfo, whisperModel, reRun)


# C:\Users\lawrence\AppData\Local\Temp\gradio
@app.get("/")
def create_chain_app():
    with gr.Blocks() as demo:
        with gr.Tab(label='上传转录'):
            with gr.Row():
                media_upload_block = gr.File(file_count='single', file_types=['audio', 'video'],
                                             label='上传媒体文件', scale=6)
            with gr.Row():
                input_textbox = gr.Textbox(label='媒体关键字', scale=10)
                input_type = gr.Dropdown(label='生成摘要类型', choices=['总体摘要', '章节摘要'], value='章节摘要',
                                         scale=2)
                rerun_type = gr.Dropdown(label='是否重跑', choices=['否', '是'], value='否', scale=1)
                submit_button = gr.Button(value='Generate', variant='primary', scale=4)

            with gr.Row():
                output_textbox1 = gr.Textbox(lines=10, label='转录文本', scale=4)
                output_textbox2 = gr.Textbox(lines=10, label='摘要文本', scale=6)

            submit_button.click(fn=doIt,
                                inputs=[input_type, media_upload_block, gr.Textbox('upload'), input_textbox,
                                        rerun_type],
                                outputs=[output_textbox1, output_textbox2])

        with gr.Tab(label='选择转录'):
            with gr.Row():
                media_select_block = gr.Dropdown(label='选择媒体文件',
                                                 choices=[''] + [f for f in os.listdir(file_default_path)
                                                                 if f.endswith('.mp4')], scale=6)
            with gr.Row():
                input_textbox = gr.Textbox(label='媒体关键字', scale=10)
                input_type = gr.Dropdown(label='生成摘要类型', choices=['总体摘要', '章节摘要'], value='章节摘要',
                                         scale=2)
                rerun_type = gr.Dropdown(label='是否重跑', choices=['否', '是'], value='否', scale=1)
                submit_button = gr.Button(value='Generate', variant='primary', scale=4)

            with gr.Row():
                output_textbox1 = gr.Textbox(lines=10, label='转录文本', scale=4)
                output_textbox2 = gr.Textbox(lines=10, label='摘要文本', scale=6)
            # print(media_select_block.value)
            submit_button.click(fn=doIt,
                                inputs=[input_type, media_select_block, gr.Textbox('choose'), input_textbox,
                                        rerun_type],
                                outputs=[output_textbox1, output_textbox2])

    return demo


io = create_chain_app()
CUSTOM_PATH = "/sotawork"
app = gr.mount_gradio_app(app, io, path=CUSTOM_PATH)
