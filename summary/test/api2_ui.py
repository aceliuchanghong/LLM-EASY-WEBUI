import gradio as gr
import requests
import tempfile


def process_media_file(file_obj):
    url3 = "http://112.48.199.7:8083/video"
    need_spk = True
    try:
        # 根据文件类型选择适当的 MIME 类型
        mime_type = 'video/mp4' if file_obj.name.endswith('.mp4') else 'audio/mpeg'
        files = [('files', (file_obj.name, open(file_obj, 'rb'), mime_type))]
        data = {
            'initial_prompt': 'deepseek,语音',
            'mode': 'timeline',
            'need_spk': need_spk
        }
        response = requests.post(url3, files=files, data=data)
        if response.status_code == 200:
            info_list = response.json().get('information', [])
            # 将信息列表合并为文本
            result_text = "\n".join(str(i) for i in info_list)
            # 将结果写入临时文件
            temp = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix='.txt')
            temp.write(result_text)
            temp.close()
            return result_text, temp.name  # 返回结果文本和临时文件路径
        else:
            error_msg = f"Error: {response.text} {response.status_code}"
            return error_msg, None
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        return error_msg, None


if __name__ == '__main__':
    # 创建Gradio界面
    # python api2_ui.py
    iface = gr.Interface(
        fn=process_media_file,
        inputs=gr.File(file_types=['audio', '.mp4'], label="上传媒体文件"),
        outputs=[
            gr.Textbox(label="结果", info="大约需要3mins"),
            gr.File(label="下载结果为TXT")
        ],
        title="媒体文件转录",
        description="上传媒体文件，处理并获取结果。"
    )

    iface.launch(server_port=913, server_name="0.0.0.0")
