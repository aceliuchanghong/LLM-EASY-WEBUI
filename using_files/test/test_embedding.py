import os

from langchain_community.embeddings import DeepInfraEmbeddings

DEEPINFRA_API_KEY = os.getenv('DEEPINFRA_API_KEY')

embeddings = DeepInfraEmbeddings(
    model_id="BAAI/bge-large-en-v1.5",
    query_instruction="",
    embed_instruction="",
)

docs = ["中文效果?"]
document_result = embeddings.embed_documents(docs)
print(document_result)

"""
https://python.langchain.com/docs/modules/data_connection/retrievers/vectorstore/
https://medium.com/@cch.chichieh/rag%E5%AF%A6%E4%BD%9C%E6%95%99%E5%AD%B8-langchain-llama2-%E5%89%B5%E9%80%A0%E4%BD%A0%E7%9A%84%E5%80%8B%E4%BA%BAllm-d6838febf8c4
"""
