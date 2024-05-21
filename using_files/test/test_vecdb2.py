from langchain_community.embeddings import DeepInfraEmbeddings
from langchain_community.vectorstores import Milvus
from langchain_openai import ChatOpenAI

from chatAll import config
from chatAll.utils import getChain
from chatAll.vecdb import load_file, get_split_docs

test_md = r'C:\Users\lawrence\PycharmProjects\LLM-EASY-WEBUI\using_files\data\00.txt'
data = load_file(test_md)
split_docs = get_split_docs(data)
COLLECTION_NAME = 'god'

embeddings = DeepInfraEmbeddings(model_id=config.EMBEDDING_MODEL)
connection_args = {'uri': config.MilvusClientUrl, 'token': config.MILVUS_API_TOKEN}
vector_store = Milvus(
    embedding_function=embeddings,
    connection_args=connection_args,
    collection_name=COLLECTION_NAME,
    drop_old=True,
).from_documents(
    split_docs,
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    connection_args=connection_args,
)
query = "夸告矢找谁?"
retriever = vector_store.as_retriever()
llm = ChatOpenAI(
    base_url=config.LLM_BASE_URL,
    api_key=config.DEEPINFRA_API_KEY,
    model=config.LLM_MODEL_NAME
)
chain = getChain(retriever, llm)
print(chain.invoke({"question": query}))
