import gradio as gr
import os
from datetime import datetime
from summary.text_sum.allSummaryWorker import allTextSummaryWorker
from summary.util.check_db import check, excute_sqlite_sql
from summary.util.mp3_from_mp4 import get_mp3_from_mp4
from summary.util.text_from_mp3 import get_whisper_model, get_whisper_text
from summary.config import (model_size_or_path,
                            table_select_sum_sql,
                            table_del_url_sql,
                            table_add_sql,
                            create_table_sql,
                            table_select_text_sql)
from summary.util.create_llm import get_llm

file_default_path = '/home/liuchanghong/media_files'
file_default_path2 = r'C:\Users\lawrence\Videos'

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


def doItTest(summary_type, file_Path, file_Info=None, re_run=False):
    if file_Path.endswith('.mp3'):
        print('mp3', file_Path)
    else:
        print('mp4', file_Path)

    summaryType = SummaryType[summary_type]
    fileInfo = file_Info
    reRun = reRunType[re_run]
    print(summaryType, fileInfo, reRun)
    return "00", "11"


def create_chain_app():
    """
    whisper_model
    :return:
    """
    with gr.Blocks() as demo:
        with gr.Tab(label='Transcribe Tab'):
            with gr.Row():
                # C:\Users\lawrence\AppData\Local\Temp\gradio
                media_upload_block = gr.File(file_count='single', file_types=['audio', 'video'],
                                             label='上传媒体文件')
                media_select_block = gr.Dropdown(label='或者选择媒体文件',
                                                 choices=[''] + [f for f in os.listdir(file_default_path2)
                                                                 if f.endswith(('.mp4', '.mp3'))])
            with gr.Row():
                input_textbox = gr.Textbox(label='媒体文件描述', scale=10)
                input_type = gr.Dropdown(label='生成摘要类型', choices=['总体摘要', '章节摘要'], value='章节摘要',
                                         scale=2)
                rerun_type = gr.Dropdown(label='是否重跑', choices=['否', '是'], value='否', scale=1)
                submit_button = gr.Button(value='Generate', variant='primary', scale=4)

            with gr.Row():
                output_textbox1 = gr.Textbox(lines=10, label='媒体文本', scale=4)
                output_textbox2 = gr.Textbox(lines=10, label='摘要文本', scale=6)

            # Add visibility changing functions
            def toggle_upload_visibility(x):
                media_select_block.visible = False
                media_upload_block.visible = True

            def toggle_select_visibility(x):
                media_upload_block.visible = False
                media_select_block.visible = True

            media_upload_block.change(fn=toggle_upload_visibility, inputs=media_upload_block,
                                      outputs=media_select_block)
            media_select_block.change(fn=toggle_select_visibility, inputs=media_select_block,
                                      outputs=media_upload_block)

            submit_button.click(fn=doItTest,
                                inputs=[input_type, media_upload_block, input_textbox, rerun_type],
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
