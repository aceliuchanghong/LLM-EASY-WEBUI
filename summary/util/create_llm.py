from langchain_openai import ChatOpenAI

from summary.config import llm_model_name, openai_api_base


def get_llm(model=llm_model_name, openai_api_base=openai_api_base):
    llm = ChatOpenAI(model=model, openai_api_base=openai_api_base, max_tokens=4096)
    return llm
