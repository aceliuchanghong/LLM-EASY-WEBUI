import gradio as gr
from smain import main
from summary.util.check_db import excute_sqlite_sql
from summary.util.mp3_from_mp4 import get_media_files
from summary.util.text_from_mp3 import get_whisper_model
from summary.config import (model_size_or_path,
                            file_default_path, company_name, create_table_sql)
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

    summaryType = SummaryType[summary_type]
    fileInfo = file_Info
    reRun = reRunType[re_run]
    print(summaryType, fileInfo, reRun)
    whisperModel = get_whisper_model(model_size_or_path)

    return main(summaryType, file_Path, fileInfo, whisperModel, reRun)


# C:\Users\lawrence\AppData\Local\Temp\gradio
@app.get("/")
def create_chain_app():
    with gr.Blocks(title=company_name) as demo:
        with gr.Tab(label='上传转录'):
            with gr.Row():
                media_upload_block = gr.File(file_count='single', file_types=['audio', 'video'],
                                             label='上传媒体文件', scale=6)
                media_upload_block.GRADIO_CACHE = file_default_path
                video_component = gr.Video(label='视频预览', scale=3)
                audio_component = gr.Audio(label='音频预览', scale=3)

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
                                inputs=[input_type, media_upload_block, gr.Textbox('upload', visible=False),
                                        input_textbox,
                                        rerun_type],
                                outputs=[output_textbox1, output_textbox2])
            media_upload_block.upload(fn=lambda x: x, inputs=[media_upload_block], outputs=[video_component])
            media_upload_block.upload(fn=lambda x: x, inputs=[media_upload_block], outputs=[audio_component])

        with gr.Tab(label='选择转录'):
            with gr.Row():
                media_files = get_media_files(file_default_path)
                media_select_block = gr.Dropdown(label='选择媒体文件',
                                                 choices=media_files, scale=6)
                video_preview = gr.Video(label='视频预览', scale=3)
                audio_preview = gr.Audio(label='音频预览', scale=3)

                # Add a preview button to play the selected media file
                preview_button = gr.Button(value='预览', variant='secondary', scale=2)
                preview_button.click(fn=lambda x: (f'{file_default_path}/{x}', f'{file_default_path}/{x}'),
                                     inputs=[media_select_block],
                                     outputs=[video_preview, audio_preview])

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
                                inputs=[input_type, media_select_block, gr.Textbox('choose', visible=False),
                                        input_textbox,
                                        rerun_type],
                                outputs=[output_textbox1, output_textbox2])

    return demo


io = create_chain_app()
CUSTOM_PATH = "/" + company_name
excute_sqlite_sql(create_table_sql)
app = gr.mount_gradio_app(app, io, path=CUSTOM_PATH)
