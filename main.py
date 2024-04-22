import os
import chromadb
import config
import gradio as gr
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core import Settings
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


def load_documents(directory=config.DATA_PATH):
    if not os.path.exists(CHROMA_DIR):
        print("Creating index...")

        documents = SimpleDirectoryReader(directory).load_data()
        chroma_collection = initiate_db()
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, transformations=[text_splitter]
        )
    else:
        print("Index found, loading...")
        chroma_collection = initiate_db()
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        index = VectorStoreIndex.from_vector_store(
            vector_store,
        )
    print(index)
    return index


def chatbot(input_text, history):
    memory = ChatMemoryBuffer.from_defaults(token_limit=3900)
    response = index.as_chat_engine(chat_mode="condense_plus_context", memory=memory, verbose=False).chat(input_text)

    return response.response


if __name__ == '__main__':
    llm = DeepInfra(model_id=config.MODEL)
    llm.model_kwargs = {
        "temperature": 0.7,
        "top_p": 0.9,
    }
    Settings.llm = llm

    embeddings = DeepInfraEmbeddings(
        model_id=config.EMBEDDING_MODEL,
        query_instruction="",
        embed_instruction="",
    )
    Settings.embed_model = embeddings

    Settings.chunk_size = 1024
    text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
    Settings.text_splitter = text_splitter

    index = load_documents()
    chat = gr.ChatInterface(fn=chatbot, title=TITLE + " ChatBot")
    chat.launch(share=False, server_name='0.0.0.0', ssl_verify=False)
