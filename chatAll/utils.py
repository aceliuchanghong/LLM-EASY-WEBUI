import gradio as gr
import os
from langchain_openai import ChatOpenAI

from chatAll import config

DEEPINFRA_API_KEY = os.getenv('DEEPINFRA_API_KEY')

model = ChatOpenAI(
    base_url="https://api.deepinfra.com/v1/openai",
    api_key=DEEPINFRA_API_KEY,
    model="meta-llama/Meta-Llama-3-70B-Instruct"
)


def add_text(history, text):
    """
    Adds the user's input text to the chat history.

    Args:
        history (list): List of tuples representing the chat history.
        text (str): The user's input text.

    Returns:
        list: Updated chat history with the new user input.
    """
    if not text:
        raise gr.Error('Enter text')
    history.append((text, ''))
    return history


def generate_response(history, query):
    """
    Generates a response based on the chat history and user's query.

    Args:
        history (list): List of tuples representing the chat history.
        query (str): The user's query.
    Returns:
        tuple: Updated chat history with the generated response and the next page number.
    """

    # Convert the history to the format expected by the model
    context = "\n".join([f"User: {user}\nAssistant: {assistant}" for user, assistant in history])
    context += f"\nUser: {query}\nAssistant:"

    # print(context)
    response = model.invoke(context)
    generated_response = response.content

    # Update the history with the generated response
    history.append((query, generated_response))

    # Yield the updated history and a placeholder for the next page number
    yield history, " "


def get_text_files(file_default_path):
    text_filess_short = {}
    text_files = []
    for root, dirs, files in os.walk(file_default_path):
        for f in files:
            file_path = os.path.join(root, f)
            if file_path.endswith(tuple(config.upload_type)):
                relative_path = os.path.relpath(file_path, file_default_path)
                # 提取上层目录的后四位和文件名
                # 首先分割路径，得到目录名和文件名
                dirs, filename = os.path.split(relative_path)
                # 然后再次分割目录名，得到上层目录的后四位
                last_four_dirs = os.path.split(dirs)[-1][-4:]
                # 组合上层目录的后四位和文件名
                result = os.path.join(last_four_dirs, filename)

                text_filess_short[result] = relative_path
                text_files.append(result)

    # print(text_filess_short, text_files)
    return text_filess_short, text_files


def upload_file(file, rerun='否'):
    # 读取文件内容
    # print(file, rerun)
    return read_file(file)


def read_file(file):
    encodings = ['utf-8', 'gbk']  # 尝试的编码格式列表
    for encoding in encodings:
        try:
            with open(file, encoding=encoding) as f:
                content = f.read()
            return content
        except UnicodeDecodeError:
            # 如果以当前编码格式读取文件失败，则尝试下一个编码格式
            continue
    # 如果所有编码格式都失败，则抛出异常
    return "Could not decode file with specified encodings"


def choose_file(file, text_files_short):
    # 替换字符串中的单引号为双引号，以符合Python字典的格式
    str_value = text_files_short.replace("'", '"')
    import ast
    # 使用ast.literal_eval()将字符串转换为字典
    dict_value = ast.literal_eval(str_value)

    # print(dict_value.get(file))
    # 读取文件内容
    file_path = config.file_default_path + "/" + dict_value.get(file)
    return read_file(file_path)


def generate_response_with_file(history, query):
    """
    Generates a response based on the chat history and user's query.

    Args:
        history (list): List of tuples representing the chat history.
        query (str): The user's query.
    Returns:
        tuple: Updated chat history with the generated response and the next page number.
    """

    # Convert the history to the format expected by the model
    context = "\n".join([f"User: {user}\nAssistant: {assistant}" for user, assistant in history])
    context += f"\nUser: {query}\nAssistant:"

    # print(context)
    response = model.invoke(context)
    generated_response = response.content

    # Update the history with the generated response
    history.append((query, generated_response))

    # Yield the updated history and a placeholder for the next page number
    yield history, " "


def clear_history(history):
    history.clear()
    return history, ""


if __name__ == '__main__':
    history = [("我的猫咪叫suy", "猫咪叫suy")]
    query = "我的猫咪叫什么？"

    for updated_history, _ in generate_response(history, query):
        print(updated_history)
