from langchain_openai import ChatOpenAI

baseURL = 'http://112.48.199.70:11434/v1/'
apiKey = 'qwen:72b'
llm = ChatOpenAI(
    base_url=baseURL,
    api_key=apiKey,
    model="qwen:72b"
)

print(llm.invoke("你好").content)

