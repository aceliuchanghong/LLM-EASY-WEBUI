import gradio as gr
import os
from using_files.test.test_llm import ChatCompletion
import time

# Load environment variables
DEEPINFRA_API_KEY = os.getenv('DEEPINFRA_API_KEY')

# Initialize the language model
llm = ChatCompletion(
    temperature=0.9,
    model="meta-llama/Meta-Llama-3-70B-Instruct",
    api_key=DEEPINFRA_API_KEY,
    base_url="https://api.deepinfra.com/v1/openai",
)


def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)


def add_message(history, message):
    # print(history)
    for x in message["files"]:
        history.append(((x,), None))
    if message["text"] is not None:
        history.append((message["text"], None))
    return history, gr.MultimodalTextbox(value=None, interactive=False)


def bot(history):
    prompt = ""
    for i, item in enumerate(history):
        if i % 2 == 0:  # User message (even indices)
            if isinstance(item[0], tuple):  # File message
                prompt += "User: [file]\n"  # Replace with file name or a generic file indicator
            else:  # Text message
                prompt += "User: " + item[0] + "\n"
        else:  # Assistant message (odd indices)
            if item[1] is not None:  # Check if response is not None
                prompt += "Assistant: " + item[1] + "\n"
            else:
                prompt += "Assistant: \n"  # or some other default value
    print("prompt:\n" + prompt)
    response = llm(prompt).choices[0].message.content
    history.append(("", ""))  # Append an empty response to the history
    for character in response:
        history[-1] = (history[-1][0], history[-1][1] + character)  # Update the last element of the history
        time.sleep(0.01)  # Simulate typing effect
        yield history
    yield history


def clear_history(history):
    history.clear()
    return history, []


def create_app():
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot(
            [],
            elem_id="chatbot",
            avatar_images=(None, (os.path.join(os.path.dirname(__file__), "../img", "avatar.jpg"))),
            bubble_full_width=False,
            height="800px",
        )
        with gr.Row():
            chat_input = gr.MultimodalTextbox(scale=10, interactive=True, file_types=["image"],
                                              placeholder="输入聊天信息或者上传文件...", show_label=False)
            btn_clear_his = gr.Button(scale=2, value="Clear", variant="secondary")

            chat_msg = chat_input.submit(add_message, [chatbot, chat_input], [chatbot, chat_input])
            bot_msg = chat_msg.then(bot, chatbot, chatbot, api_name="bot_response")
            bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input])

            btn_clear_his.click(clear_history, inputs=chatbot, outputs=[chatbot, chatbot])
            chatbot.like(print_like_dislike, None, None)
    return demo


if __name__ == "__main__":
    app = create_app()
    app.launch(share=False)
