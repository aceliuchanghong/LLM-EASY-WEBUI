from langchain_openai import ChatOpenAI


def get_llm(model="gpt-4-turbo", openai_api_base="https://api.xty.app/v1"):
    llm = ChatOpenAI(model=model, openai_api_base=openai_api_base)
    return llm
