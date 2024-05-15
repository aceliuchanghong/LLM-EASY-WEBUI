import time
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DeepInfraEmbeddings
from chatAll import config

embeddings = DeepInfraEmbeddings(
    model_id=config.EMBEDDING_MODEL
)


def load_file(file_path):
    if file_path.endswith(tuple(['.md', '.txt'])):
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


def get_split_docs(data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100, add_start_index=True)
    split_docs = text_splitter.split_documents(data)
    return split_docs


def get_chunk(split_docs):
    # https://milvus.io/docs/quickstart.md
    """
    "embeddings":
    [[
      0.0,
      0.5,
      1.0
    ],[
      1.0,
      0.5,
      0.0
    ],...]
    怎么插入呢?之后考虑
    :param split_docs:
    :return:
    """
    chunks = []
    dit = {}
    for split_doc in split_docs:
        embeddings_chunk_idx = split_doc.metadata['start_index']
        embeddings_result = embeddings.embed_documents(split_doc.page_content)
        embeddings_chunk = split_doc.page_content
        embeddings_file_source = split_doc.metadata['source']

        dit['id'] = embeddings_chunk_idx
        dit['vector'] = embeddings_result
        dit['text'] = embeddings_chunk
        dit['dim'] = len(embeddings_result[0])
        dit['file'] = embeddings_file_source
        chunks.append(dit)
    return chunks


def db_insert(file_name, dimension, chunks, metric_type):
    pass


if __name__ == '__main__':
    # 测试数据
    test_txt = '../using_files/data/00.txt'
    test_txt2 = r'C:\Users\lawrence\PycharmProjects\FAQ_Of_LLM_Interview\pytorch\data\books\hongLouMeng.txt'
    test_md = r'C:\Users\lawrence\Desktop\travel_tips\travel_tips.md'
    test_pdf = r'C:\Users\lawrence\Desktop\别人简历\简历-桂先生.pdf'
    test_py = 'config.py'

    start = time.time()
    data = load_file(test_txt)
    split_docs = get_split_docs(data)
    for doc in split_docs:
        print(doc)
        print(doc.metadata['source'])
        print(doc.metadata['start_index'])
        print(doc.page_content)
    print(get_chunk(split_docs))
    end = time.time()

    execution_time_seconds = end - start
    execution_time_minutes = execution_time_seconds // 60
    execution_time_seconds %= 60

    print(f"Execution time: {int(execution_time_minutes)} minutes and {execution_time_seconds:.2f} seconds")
