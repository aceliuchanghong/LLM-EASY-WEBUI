import os
from openai import OpenAI

DEEPINFRA_API_KEY = os.getenv('DEEPINFRA_API_KEY')


class ChatCompletion:
    def __init__(self, temperature, model, api_key, base_url, max_tokens=51200, stream=False):
        self.temperature = temperature
        self.model = model
        self.openai = OpenAI(api_key=api_key, base_url=base_url)
        self.stream = stream
        self.max_tokens = max_tokens

    def __call__(self, prompt):
        messages = [{"role": "user", "content": prompt}]
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
