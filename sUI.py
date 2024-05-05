import gradio as gr
import os
from datetime import datetime

from smain import main
from summary.text_sum.allSummaryWorker import allTextSummaryWorker
from summary.util.check_db import check, excute_sqlite_sql
from summary.util.mp3_from_mp4 import get_mp3_from_mp4
from summary.util.text_from_mp3 import get_whisper_model, get_whisper_text
from summary.config import (model_size_or_path,
                            table_select_sum_sql,
                            table_del_url_sql,
                            table_add_sql,
                            create_table_sql,
                            table_select_text_sql,
                            file_default_path)
from summary.util.create_llm import get_llm

SummaryType = {
    "总体摘要": "SumMp4All",
    "章节摘要": "SumMp4Step",
}

reRunType = {
    "是": True,
    "否": False,
}


def doIt(whisper_model):
    pass


def doItTest(summary_type, file_Path, file_get_type='upload', file_Info=None, re_run=False):
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
def create_chain_app():
    with gr.Blocks() as demo:
        with gr.Tab(label='上传转录'):
            with gr.Row():
                media_upload_block = gr.File(file_count='single', file_types=['audio', 'video'],
                                             label='上传媒体文件', scale=6)
            with gr.Row():
                input_textbox = gr.Textbox(label='媒体文件描述', scale=10)
                input_type = gr.Dropdown(label='生成摘要类型', choices=['总体摘要', '章节摘要'], value='章节摘要',
                                         scale=2)
                rerun_type = gr.Dropdown(label='是否重跑', choices=['否', '是'], value='否', scale=1)
                submit_button = gr.Button(value='Generate', variant='primary', scale=4)

            with gr.Row():
                output_textbox1 = gr.Textbox(lines=10, label='媒体文本', scale=4)
                output_textbox2 = gr.Textbox(lines=10, label='摘要文本', scale=6)

            submit_button.click(fn=doItTest,
                                inputs=[input_type, media_upload_block, gr.Textbox('upload'), input_textbox,
                                        rerun_type],
                                outputs=[output_textbox1, output_textbox2])

        with gr.Tab(label='选择转录'):
            with gr.Row():
                media_select_block = gr.Dropdown(label='或者选择媒体文件',
                                                 choices=[''] + [f for f in os.listdir(file_default_path)
                                                                 if f.endswith('.mp4')], scale=6)
            with gr.Row():
                input_textbox = gr.Textbox(label='媒体文件描述', scale=10)
                input_type = gr.Dropdown(label='生成摘要类型', choices=['总体摘要', '章节摘要'], value='章节摘要',
                                         scale=2)
                rerun_type = gr.Dropdown(label='是否重跑', choices=['否', '是'], value='否', scale=1)
                submit_button = gr.Button(value='Generate', variant='primary', scale=4)

            with gr.Row():
                output_textbox1 = gr.Textbox(lines=10, label='媒体文本', scale=4)
                output_textbox2 = gr.Textbox(lines=10, label='摘要文本', scale=6)
            # print(media_select_block.value)
            submit_button.click(fn=doItTest,
                                inputs=[input_type, media_select_block, gr.Textbox('choose'), input_textbox,
                                        rerun_type],
                                outputs=[output_textbox1, output_textbox2])
        with gr.Tab(label='Structure Tab'):
            img = gr.Image(value='using_files/img/img.png', label='项目结构')

    return demo


if __name__ == '__main__':
    # whisper_model = get_whisper_model(model_size_or_path)
    # excute_sqlite_sql(create_table_sql)
    #
    # app = create_chain_app(whisper_model)
    app = create_chain_app()
    app.launch(server_name="0.0.0.0", server_port=2333, share=False)