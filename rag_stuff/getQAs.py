import os
from langchain_openai import ChatOpenAI
import time
import re
import json
import csv

_instance = None


def get_instance():
    global _instance
    if _instance is None:
        _instance = ChatOpenAI(model='qwen2', api_key='qwen2', openai_api_base="http://192.168.18.106:11434/v1/")
    return _instance


def get_files(file_path_dir, start_suffix=None, suffix=None, go_over_dir=False):
    files_with_suffix = []
    for root, dirs, files in os.walk(file_path_dir):
        for file in files:
            if start_suffix is not None and suffix is not None:
                if file.startswith(start_suffix) and file.endswith(suffix):
                    files_with_suffix.append(os.path.join(root, file).replace("\\", '/'))
            elif start_suffix is not None and file.startswith(start_suffix):
                files_with_suffix.append(os.path.join(root, file).replace("\\", '/'))
            elif suffix is not None and file.endswith(suffix):
                files_with_suffix.append(os.path.join(root, file).replace("\\", '/'))
        if not go_over_dir:
            break
    return files_with_suffix


def parse_qa_response(response):
    qa_pairs = []
    pattern = re.compile(r"Q:(.*?)\nA:(.*?)\n", re.DOTALL)
    matches = pattern.findall(response)

    for match in matches:
        question, answer = match
        qa_pair = {
            "instruction": question.strip(),
            "input": "",
            "output": answer.strip()
        }
        qa_pairs.append(qa_pair)

    return qa_pairs


def get_QA(file_path, prompt=None):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    llm = get_instance()
    if prompt is None:
        prompt = ("你是一个专业的研究人员,帮我就以下内容生成适当数量的问题和对应答案,其问题和答案应该\n"
                  "1.遵循以下格式:\nQ:<问题><换行>A:<答案>\n"
                  "2.没有其他多余的符号和文字\n以下是具体内容：\n")
    prompt_to_llm = prompt + file_content

    response = llm.invoke(prompt_to_llm).content
    print(response)
    qa_pairs = parse_qa_response(response + "\n")
    return qa_pairs


if __name__ == '__main__':
    start = time.time()
    file_path_dir = r'D:\aProject\py\myDeepdoc\ocr_outputs'
    start_suffix = '火炬电子书-2024-总第137期-新春特刊.pdf_'
    suffix = '.txt'
    go_over_dir = False
    ans = []
    null_text = []
    my_ocr_list = get_files(file_path_dir, start_suffix, suffix, go_over_dir)
    # my_ocr_list = ['D:/aProject/py/myDeepdoc/ocr_outputs/火炬电子书-2024-总第137期-新春特刊.pdf_0.jpg.txt']
    for i in range(0, len(my_ocr_list)):
        this_ans = get_QA(my_ocr_list[i])
        if len(this_ans) == 0:
            print("running again:", my_ocr_list[i])
            this_ans = get_QA(my_ocr_list[i])
            if len(this_ans) == 0:
                null_text.append(my_ocr_list[i])
        print(this_ans)
        ans += this_ans
    # 写入json
    with open('QA.json', 'w', encoding='utf-8') as file:
        json.dump(ans, file, ensure_ascii=False, indent=4)
    # 写入CSV
    with open('QA.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 写入表头 writer.writerow(['instruction', 'output'])
        for item in ans:
            writer.writerow([item['instruction'], item['output']])

    if len(null_text) > 0:
        print(null_text)
    end = time.time()
    print('\ncost:', end - start)
