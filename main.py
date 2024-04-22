import os
import time
import chromadb
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config
import gradio as gr
from langchain_community.llms import DeepInfra
from langchain_community.embeddings import DeepInfraEmbeddings

CHROMA_DIR = config.CHROMA_DIR
DB_NAME = config.DATA_NAME
TITLE = config.DATA_NAME
DATA_PATH = config.DATA_PATH


def initiate_db():
    db = chromadb.PersistentClient(path=CHROMA_DIR)
    chroma_collection = db.get_or_create_collection(DB_NAME)
    return chroma_collection


def load_documents(directory=DATA_PATH):
    loader = DirectoryLoader(directory)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024, chunk_overlap=100, add_start_index=True
    )
    split_docs = text_splitter.split_documents(documents)
    return split_docs


if __name__ == '__main__':
    llm = DeepInfra(model_id=config.MODEL)
    llm.model_kwargs = {
        "temperature": 0.7,
        "top_p": 0.9,
    }

    embeddings = DeepInfraEmbeddings(
        model_id=config.EMBEDDING_MODEL,
        query_instruction="",
        embed_instruction="",
    )
    start = time.time()
    split_docs = load_documents('using_files/data')
    for doc in split_docs:
        print(doc)
    end = time.time()
    print(f"数据切分时间：{(end - start) / 60 % 60:.4f}分({end - start:.4f}秒)")

    chroma_collection = initiate_db()

    # start_embedding = time.time()
    # embedded_docs = []
    # i = 0
    # for doc in split_docs:
    #     doc_list = [doc.page_content]
    #     print(doc_list)
    #     embeddings_list = embeddings.embed_documents(doc_list)
    #     embedded_docs.append({
    #         "id": str(i),
    #         "text": doc.page_content,
    #         "embedding": embeddings_list[0]
    #     })
    #     i += 1
    # print(embedded_docs)
    # end_embedding = time.time()
    # print(f"嵌入时间：{(end_embedding - start_embedding) / 60 % 60:.4f}分({end_embedding - start_embedding:.4f}秒)")
    #
    # start_indexing = time.time()
    # for doc in embedded_docs:
    #         chroma_collection.add(ids=[doc['id']], documents=[doc['text']], embeddings=[doc['embedding']])
    # end_indexing = time.time()
    # print(f"索引时间：{(end_indexing - start_indexing) / 60 % 60:.4f}分({end_indexing - start_indexing:.4f}秒)")
