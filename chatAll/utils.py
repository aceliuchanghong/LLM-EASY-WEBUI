import gradio as gr
import os
from langchain_openai import ChatOpenAI
import time

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


def clear_history(history):
    history.clear()
    return history, ""


if __name__ == '__main__':
    history = [("我的猫咪叫suy", "猫咪叫suy")]
    query = "我的猫咪叫什么？"

    for updated_history, _ in generate_response(history, query):
        print(updated_history)
