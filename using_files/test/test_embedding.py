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
