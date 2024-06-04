from langchain_openai import ChatOpenAI

from summary.config import llm_model_name, openai_api_base, max_tokens, apiKey


def get_llm(model=llm_model_name, openai_api_base=openai_api_base):
    llm = ChatOpenAI(model=model,
                     openai_api_base=openai_api_base,
                     api_key=apiKey,
                     max_tokens=max_tokens)
    return llm
