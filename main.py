import gradio as gr
import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chatAll import config
from chatAll.utils import (add_text,
                           generate_response,
                           clear_history,
                           generate_response_with_file,
                           upload_file, get_text_files, choose_file)

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


def getChain(retriever, llm):
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
    with gr.Blocks(title="Chatbot") as demo:
        with gr.Tab(label='Chat-Tab'):
            text_chatbot1 = gr.Chatbot(
                [],
                label="chatBot",
                elem_id="chatBot",
                avatar_images=((os.path.join(os.path.dirname(__file__), "using_files/img", "user.png")),
                               (os.path.join(os.path.dirname(__file__), "using_files/img", "avatar.jpg"))),
                bubble_full_width=False,
                height="600px",
            )

            with gr.Row():
                chat_text_input1 = gr.Textbox(scale=10, interactive=True, lines=3, show_label=False, render=False,
                                              placeholder="愿起一剑杀万劫...")
                gr.Examples(config.examples, chat_text_input1, label='示例')
            with gr.Row():
                chat_text_input1.render()
                text_submit_button1 = gr.Button(value='Chat', variant='primary', scale=4)
                text_clear_button1 = gr.Button(scale=2, value="Clear", variant="secondary")

        with gr.Tab(label='File-Chat-Tab'):
            with gr.Row():
                filechatbot = gr.Chatbot(
                    [],
                    label="fileChatBot",
                    elem_id="fileChatBot",
                    avatar_images=((os.path.join(os.path.dirname(__file__), "using_files/img", "user.png")),
                                   (os.path.join(os.path.dirname(__file__), "using_files/img", "avatar.jpg"))),
                    bubble_full_width=False,
                    height=550,
                )
                show_text = gr.Textbox(label='File Preview', lines=24, placeholder=config.article,
                                       interactive=True)

            with gr.Row():
                file_chat_input = gr.Textbox(render=False, scale=10, placeholder="因为困难多壮志...", lines=5,
                                             show_label=False, interactive=True, )
                gr.Examples(config.examples2, file_chat_input)
            with gr.Row():
                text_files_short, text_files = get_text_files(config.file_default_path)
                file_chat_input.render()
                submit_btn = gr.Button(value='Chat', variant='primary', scale=5)
                with gr.Column(scale=1):
                    upload_type = gr.Dropdown(label='重新上传文件', choices=['否', '是'], value='否', scale=1)
                    upload_btn = gr.UploadButton("📁 Upload", file_types=config.upload_type, scale=1)
                with gr.Column(scale=1):
                    choose_btn = gr.Dropdown(label='📁 Choose', choices=text_files, scale=1)
                    preview_btn = gr.Button(value='预览选择文件', scale=1)
                upload_btn.GRADIO_CACHE = config.file_default_path
                btn_clear_his = gr.Button(scale=2, value="Clear", variant="secondary")

        with gr.Tab(label='Structure-Tab'):
            img = gr.Image('using_files/img/img.png')
        # 第一个模块
        # queue=False参数，这意味着点击按钮后，只有当当前事件处理完成后，才能再次点击按钮。
        text_submit_button1.click(add_text, inputs=[text_chatbot1, chat_text_input1], outputs=[text_chatbot1],
                                  queue=False).success(generate_response, inputs=[text_chatbot1, chat_text_input1],
                                                       outputs=[text_chatbot1, chat_text_input1])
        text_clear_button1.click(clear_history, inputs=text_chatbot1, outputs=[text_chatbot1, chat_text_input1])

        # 第二个模块
        upload_btn.upload(upload_file, [upload_btn, upload_type], show_text)
        preview_btn.click(choose_file, inputs=[choose_btn, gr.Textbox(text_files_short, visible=False)],
                          outputs=show_text)

        # chat_msg = file_chat_input.submit(add_text_with_file, [filechatbot, file_chat_input],
        #                                   [filechatbot, show_text, file_chat_input])

    return demo


if __name__ == "__main__":
    app = create_chain_app()
    app.launch(server_name="0.0.0.0", server_port=2333, share=False)
    # start = time.time()
    # split_docs = load_documents('using_files/data')
    # for doc in split_docs:
    #     print(doc)
    # end = time.time()
    # print(f"数据切分时间：{(end - start) / 60 % 60:.4f}分({end - start:.4f}秒)")
    # retriever = get_retriever(split_docs, embedding)
    # chain = getChain(retriever)
