# way1
from langchain_openai import ChatOpenAI
from flagged.pass2 import deepseek

llm = ChatOpenAI(model="gpt-4-turbo",
                 openai_api_base="https://api.xty.app/v1")

print(llm.invoke("hello").content)

# print(llm.get_num_tokens("你好"))
# print(llm.get_num_tokens("nihao"))
# print(llm.get_num_tokens("vxerbui"))

# way2
from openai import OpenAI

client = OpenAI(api_key=deepseek, base_url="https://api.deepseek.com/")
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ]
)
print(response.choices[0].message.content)

# way3
from langchain_openai import ChatOpenAI

llm2 = ChatOpenAI(model="deepseek-chat",
                  api_key=deepseek,
                  base_url="https://api.deepseek.com/")

print(llm2.invoke("你好").content)

# way4
import os
from langchain_openai import ChatOpenAI

DEEPINFRA_API_KEY = os.getenv('DEEPINFRA_API_KEY')

llm3 = ChatOpenAI(
    base_url="https://api.deepinfra.com/v1/openai",
    api_key=DEEPINFRA_API_KEY,
    model="meta-llama/Meta-Llama-3-70B-Instruct"
)
print(llm3.invoke("你好").content)
