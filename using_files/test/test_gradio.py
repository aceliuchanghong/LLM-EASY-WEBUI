import random

import gradio as gr
import os
import time


def generate_text(history, txt):
    history.append([txt, ""])
    yield from bot(history)


def generate_image(history, file):
    # assume file is a PIL.Image object
    img = file  # replace with your image generation logic
    history.append(["", img])
    yield history


def bot(history):
    message = history[-1][0]
    # 如果最后一条消息是一个元组类型，通常这种情况下代表文件上传成功，因为上传成功后往往返回的是元组数据，比如 (文件名, 文件大小)
    if isinstance(message, tuple):
        response = "文件上传成功"
    else:
        history_true = history[:-1]
        prompt = history[-1][0]
        input_data = {"history": history_true, "prompt": prompt}
        response = random.choice(["How are you?", "I love you", "I'm very hungry"])
    history[-1][1] = ""
    for character in response:
        history[-1][1] += character
        time.sleep(0.05)
        yield history


def clear_history(history):
    return []


def create_app():
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot(
            [],
            elem_id="chatbot",
            bubble_full_width=False,
            avatar_images=(None, (os.path.join(os.path.dirname(__file__), "../img", "avatar.jpg"))),
        )
        with gr.Row():
            btn = gr.UploadButton("📁", scale=3, file_types=["text"])

            txt = gr.Textbox(
                scale=20,
                show_label=False,
                label="chatInfo",
                placeholder="输入文字",
                container=False,
            )

            btn_submit_text = gr.Button(scale=6, value="Generate Text", variant="primary")
            btn_submit_img = gr.Button(scale=3, value="Generate Img", variant="secondary")
            btn_clear_his = gr.Button(scale=2, value="Clear", variant="secondary")

            btn_submit_text.click(generate_text, inputs=[chatbot, txt], outputs=chatbot)
            btn_submit_img.click(generate_image, inputs=[chatbot, txt], outputs=chatbot)
            btn_clear_his.click(clear_history, inputs=chatbot, outputs=chatbot)

            btn_enter_text = txt.submit(generate_text, inputs=[chatbot, txt], outputs=chatbot)

    return demo


if __name__ == '__main__':
    app = create_app()
    app.launch(share=False)
