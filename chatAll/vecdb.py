import time
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DeepInfraEmbeddings
from chatAll import config
from pymilvus import MilvusClient, DataType

from chatAll.utils import model

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# 创建一个控制台处理程序并设置日志级别
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# 创建一个格式化器并将其添加到处理程序
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# 将处理程序添加到记录器
logger.addHandler(ch)

embeddings = DeepInfraEmbeddings(model_id=config.EMBEDDING_MODEL)
client = MilvusClient(
    uri=config.MilvusClientUrl,
    token=config.MILVUS_API_TOKEN
)


def load_file(file_path):
    if file_path.endswith(tuple(['.md', '.txt'])):
        # from langchain_community.document_loaders import TextLoader
        loader = UnstructuredMarkdownLoader(file_path)
        data = loader.load()
        return data
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
        data = loader.load()
        return data
    else:
        data = [Document(page_content='no such suffix support', metadata={'source': file_path, 'start_index': 0})]
        return data


def get_split_docs(data, re_run=False):
    logger.info("Starting to split documents.")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100, add_start_index=True)
    split_docs = text_splitter.split_documents(data)
    logger.info("Documents split successfully.")
    return split_docs


# https://milvus.io/docs/quickstart.md
def get_chunk(split_docs, re_run=False):
    chunks = []
    for split_doc in split_docs:
        embeddings_chunk_idx = split_doc.metadata['start_index']
        embeddings_result = embeddings.embed_documents([split_doc.page_content])
        embeddings_chunk = split_doc.page_content
        dit = {}
        dit['my_id'] = embeddings_chunk_idx
        dit['my_vector'] = embeddings_result[0]
        dit['my_text'] = embeddings_chunk
        chunks.append(dit)
    logger.info("Embedding successfully.")
    return chunks


def db_insert(collection_name, chunks, client, metric_type='COSINE', dim=1024, max_length=20000, re_run=False):
    schema = MilvusClient.create_schema(
        auto_id=False,
        enable_dynamic_field=True,
    )
    schema.add_field(field_name="my_id", datatype=DataType.INT64, is_primary=True)
    schema.add_field(field_name="my_vector", datatype=DataType.FLOAT_VECTOR, dim=dim)
    schema.add_field(field_name="my_text", datatype=DataType.VARCHAR, max_length=max_length)
    index_params = client.prepare_index_params()
    index_params.add_index(
        field_name="my_vector",
        index_type="AUTOINDEX",
        metric_type=metric_type
    )

    # 检查当前集合
    hasIt = False
    collections = client.list_collections()
    if collection_name in collections:
        hasIt = True
    if not hasIt or re_run:
        try:
            client.drop_collection(collection_name=collection_name)
        except Exception as e:
            print(f'Milvus删除collection:{collection_name}出错', str(e))
        try:
            client.create_collection(
                collection_name=collection_name,
                schema=schema,
                index_params=index_params
            )
        except Exception as e:
            print(f'Milvus创建collection:{collection_name}时出错', str(e))
        try:
            client.insert(
                collection_name=collection_name,
                data=chunks
            )
            # {'insert_count': 3, 'ids': [0, 867, 1745]}
        except Exception as e:
            print('Milvus插入出错', str(e))
    logger.info("Insert successfully.")


if __name__ == '__main__':
    # 测试数据
    test_txt = '../using_files/data/00.txt'
    test_txt2 = r'C:\Users\lawrence\PycharmProjects\FAQ_Of_LLM_Interview\pytorch\data\books\hongLouMeng.txt'
    test_pdf = r'C:\Users\lawrence\Desktop\别人简历\简历-桂先生.pdf'
    test_py = 'config.py'
    collection_name = 'liu'
    query = "宝玉和谁结婚了?"
    # query = "夸告矢找谁?"
    output_fields = "my_text"
    re_run = False

    start = time.time()
    data = load_file(test_txt)
    split_docs = get_split_docs(data, re_run=re_run)
    chunks = get_chunk(split_docs, re_run=re_run)
    db_insert(collection_name=collection_name, chunks=chunks, client=client, re_run=re_run)
    query_vec = embeddings.embed_documents([query])
    res = client.search(
        collection_name=collection_name,
        data=query_vec,
        limit=5,
        output_fields=[output_fields]
    )

    concatenated_text = ""
    # 遍历res列表中的每个元素
    for sublist in res:
        for item in sublist:
            # 获取my_text值并拼接到concatenated_text中
            concatenated_text += item['entity'][output_fields]

    prompt = "根据以下内容给出中文回答:\n{begin}\n" + concatenated_text + "\n{end}\n问题:\n" + query + "\n不清楚就回答:DK"
    # print(prompt)
    print(query, "\n", model.invoke(prompt).content.strip())
    end = time.time()

    execution_time_seconds = end - start
    execution_time_minutes = execution_time_seconds // 60
    execution_time_seconds %= 60

    print(f"Execution time: {int(execution_time_minutes)} minutes and {execution_time_seconds:.2f} seconds")
