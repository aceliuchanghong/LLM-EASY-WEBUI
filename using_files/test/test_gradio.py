import gradio as gr
import os

from using_files.test.test_llm import ChatCompletion

DEEPINFRA_API_KEY = os.getenv('DEEPINFRA_API_KEY')

llm = ChatCompletion(temperature=0.7, model="meta-llama/Meta-Llama-3-70B-Instruct",
                     api_key=DEEPINFRA_API_KEY, base_url="https://api.deepinfra.com/v1/openai")

chat_history = []


def generate_text(history, txt):
    history.append(("User", txt))
    response = bot(history)
    history.append(("Assistant", response))
    return "", history


def generate_image(history, file):
    img = file
    history.append(("User", img))
    response = "文件上传成功"
    history.append(("Assistant", response))
    return "", history


def bot(history):
    message = history[-1][1]  # 取最后一条消息的内容
    if isinstance(message, tuple):
        response = "文件上传成功"
    else:
        prev_history = [f"{turn[0]}: {turn[1]}" for turn in history[:-1]]
        prompt = "\n".join(prev_history) + f"\nUser: {message}"
        response = llm(prompt).choices[0].message.content
        input_data = {"history": history, "prompt": prompt}
        print(input_data)
    return response


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
