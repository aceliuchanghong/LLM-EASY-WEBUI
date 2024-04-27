import os

from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import convert_to_messages
from langchain_core.prompt_values import StringPromptValue, PromptValue, ChatPromptValue
from openai import OpenAI
from typing import Sequence

DEEPINFRA_API_KEY = os.getenv('DEEPINFRA_API_KEY')


class ChatCompletion:
    def __init__(self, temperature, model, api_key, base_url, max_tokens=5126, stream=False):
        self.temperature = temperature
        self.model = model
        self.openai = OpenAI(api_key=api_key, base_url=base_url)
        self.stream = stream
        self.max_tokens = max_tokens

    def _convert_input(self, input: LanguageModelInput) -> PromptValue:
        if isinstance(input, PromptValue):
            return input
        elif isinstance(input, str):
            return StringPromptValue(text=input)
        elif isinstance(input, Sequence):
            return ChatPromptValue(messages=convert_to_messages(input))
        else:
            raise ValueError(
                f"Invalid input type {type(input)}. "
                "Must be a PromptValue, str, or list of BaseMessages."
            )

    def __call__(self, prompt):
        messages = [
            {"role": "user", "content": self._convert_input(prompt).text}
        ]
        print(messages)
        response = self.openai.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            stream=self.stream,
            max_tokens=self.max_tokens
        )
        return response


if __name__ == '__main__':
    llm = ChatCompletion(temperature=0.7, model="meta-llama/Meta-Llama-3-70B-Instruct",
                         api_key=DEEPINFRA_API_KEY, base_url="https://api.deepinfra.com/v1/openai")

    response = llm("Hello")
    print(response.choices[0].message.content)

    # llm2 = ChatCompletion(temperature=0.7, model="meta-llama/Meta-Llama-3-70B-Instruct",
    #                       api_key=DEEPINFRA_API_KEY, base_url="https://api.deepinfra.com/v1/openai", stream=True)
    #
    # response2 = llm2("Hello")
    # for event in response2:
    #     print(event.choices[0].delta.content)
