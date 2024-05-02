from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4-turbo",
                 openai_api_base="https://api.xty.app/v1")

print(llm.invoke("hello").content)
