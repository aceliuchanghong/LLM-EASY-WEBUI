from langchain_openai import ChatOpenAI
from fastapi import FastAPI
import uvicorn

app = FastAPI()
llm = ChatOpenAI(model="qwen", api_key="Qwen", base_url="http://loaclhost:11434/v1/")


@app.post("/chat")
def talk2llm(prompt):
    res = llm.invoke(prompt).content
    print(res)
    return res


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
