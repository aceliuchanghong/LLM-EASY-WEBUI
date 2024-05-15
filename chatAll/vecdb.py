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


def split_docs(data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024, chunk_overlap=100, add_start_index=True
    )
    split_docs = text_splitter.split_documents(data)
    return split_docs


def get_chunk(split_docs):
    pass


if __name__ == '__main__':
    test_txt = '../using_files/data/00.txt'
    test_md = r'C:\Users\lawrence\Desktop\travel_tips\travel_tips.md'
    test_pdf = r'C:\Users\lawrence\Desktop\别人简历\简历-桂先生.pdf'
    test_py = 'config.py'

    start = time.time()
    data = load_file(test_txt)
    split_docs = split_docs(data)
    for doc in split_docs:
        print(doc)
    end = time.time()

    execution_time_seconds = end - start
    execution_time_minutes = execution_time_seconds // 60
    execution_time_seconds %= 60

    print(f"Execution time: {int(execution_time_minutes)} minutes and {execution_time_seconds:.2f} seconds")
