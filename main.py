import gradio as gr
import os

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import DeepInfraEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config
import time

# Load environment variables
DEEPINFRA_API_KEY = os.getenv('DEEPINFRA_API_KEY')

# Initialize the language model
llm = ChatOpenAI(
    base_url="https://api.deepinfra.com/v1/openai",
    api_key=DEEPINFRA_API_KEY,
    model="meta-llama/Meta-Llama-3-70B-Instruct"
)

embedding = DeepInfraEmbeddings(
    model_id="BAAI/bge-large-en-v1.5",
    query_instruction="",
    embed_instruction="",
)

DATA_PATH = config.DATA_PATH
CHROMA_DIR = config.CHROMA_DIR


def load_documents(directory=DATA_PATH):
    loader = DirectoryLoader(directory)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024, chunk_overlap=100, add_start_index=True
    )
    split_docs = text_splitter.split_documents(documents)
    return split_docs


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_retriever(split_docs, embedding):
    db = Chroma.from_documents(documents=split_docs, embedding=embedding, persist_directory=CHROMA_DIR)
    retriever = db.as_retriever()
    # print(retriever.invoke("万清平是谁?"))
    return retriever


def getChain(retriever):
    # 修改之后的prompt模板
    prompt = PromptTemplate.from_template("""根据文本回答问题:
    {context}
    问题:
    {question}
    不清楚就回答:"DK"
    """)
    # chain
    my_chain = ({"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
                )
    # question = "夸告矢找谁?"
    # print(my_chain.invoke({"question": question}))
    return my_chain


def create_chain_app():
    with gr.Blocks() as demo:
        with gr.Tab(label='Chat Tab'):
            chatbot = gr.Chatbot(
                [],
                elem_id="chatbot",
                avatar_images=(None, (os.path.join(os.path.dirname(__file__), "../img", "avatar.jpg"))),
                bubble_full_width=False,
                height="600px",
            )
            with gr.Row():
                chat_input = gr.MultimodalTextbox(scale=10, interactive=True, file_types=["image"],
                                                  placeholder="输入聊天信息或者上传文件...", show_label=False)
        with gr.Tab(label='Secret Tab'):
            img = gr.Image('using_files/img/img.png')

    return demo


if __name__ == "__main__":
    # app = create_chain_app()
    # app.launch(server_name="0.0.0.0", server_port=2333, share=False)
    start = time.time()
    split_docs = load_documents('using_files/data')
    for doc in split_docs:
        print(doc)
    end = time.time()
    print(f"数据切分时间：{(end - start) / 60 % 60:.4f}分({end - start:.4f}秒)")
    retriever = get_retriever(split_docs, embedding)
    chain = getChain(retriever)
