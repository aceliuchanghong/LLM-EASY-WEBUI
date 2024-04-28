import os

from langchain_core.prompts import PromptTemplate
# pip install -qU langchain-openai
from langchain_openai import ChatOpenAI
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter

from using_files.test.test_embedding import embeddings

DEEPINFRA_API_KEY = os.getenv('DEEPINFRA_API_KEY')

llm = ChatOpenAI(
    base_url="https://api.deepinfra.com/v1/openai",
    api_key=DEEPINFRA_API_KEY,
    model="meta-llama/Meta-Llama-3-70B-Instruct"
)

# Load, chunk and index the contents of the blog.
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever()
prompt = PromptTemplate.from_template("""根据文本回答问题:
    {context}
    问题:
    {question}
    不清楚就回答:"DK"
    """)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
)

print(rag_chain.invoke("What is Task Decomposition?"))
