from langchain_openai import ChatOpenAI

baseURL = 'http://localhost:11434/v1/'
apiKey = 'Qwen'
llm = ChatOpenAI(
    base_url=baseURL,
    api_key=apiKey,
    model="Qwen"
)

print(llm.invoke("你好"))
