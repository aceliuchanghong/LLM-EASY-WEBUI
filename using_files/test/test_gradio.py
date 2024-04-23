import gradio as gr
import os

from using_files.test.test_llm import ChatCompletion

DEEPINFRA_API_KEY = os.getenv('DEEPINFRA_API_KEY')

llm = ChatCompletion(
    temperature=0.7,
    model="meta-llama/Meta-Llama-3-70B-Instruct",
    api_key=DEEPINFRA_API_KEY,
    base_url="https://api.deepinfra.com/v1/openai",
    stream=True
)

chat_history = []


def generate_text(history, txt):
    history.append(("User", txt))
    responses = llm("\n".join([f"{turn[0]}: {turn[1]}" for turn in history]))
    for event in responses:
        history.append(("Assistant", event.choices[0].delta.content))
    print(history)
    return "", history


def generate_image(history, file):
    img = file
    history.append(("User", img))
    response = "文件上传成功"
    history.append(("Assistant", response))
    return "", history


def clear_history():
    global chat_history
    chat_history = []
    return "", chat_history


def create_app():
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot(
            chat_history,
            elem_id="chatbot",
            bubble_full_width=False,
            avatar_images=(None, (os.path.join(os.path.dirname(__file__), "../img", "avatar.jpg"))),
            height="800px",
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
            btn_submit_text.click(generate_text, inputs=[chatbot, txt], outputs=[txt, chatbot])
            btn_submit_img.click(generate_image, inputs=[chatbot, txt], outputs=[txt, chatbot])
            btn_clear_his.click(clear_history, inputs=None, outputs=[txt, chatbot])
            btn_enter_text = txt.submit(generate_text, inputs=[chatbot, txt], outputs=[txt, chatbot])
        return demo


if __name__ == '__main__':
    app = create_app()
    app.launch(share=False)
