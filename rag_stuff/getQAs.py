import os
from langchain_openai import ChatOpenAI
import time
import re
import json
import csv
import argparse
import concurrent.futures

_instance = None


def get_instance():
    global _instance
    if _instance is None:
        _instance = ChatOpenAI(model='qwen2:72b', api_key='qwen2:72b',
                               openai_api_base="http://112.48.199.202:11434/v1/")
    return _instance


def get_or_create_directory(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


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
        prompt = ("你是一位专业的研究人员，请根据以下内容生成一系列有价值的问题及其答案。要求如下:\n"
                  "1.问题和答案的格式应为:\nQ:<问题><换行>A:<答案>\n"
                  "2.避免使用任何额外的符号或文字\n以下是具体内容：\n")
    prompt_to_llm = prompt + file_content

    response = llm.invoke(prompt_to_llm).content
    print(response)
    qa_pairs = parse_qa_response(response + "\n")
    return qa_pairs


def process_file(file, max_retries):
    retries = 0
    while retries < max_retries:
        this_ans = get_QA(file)
        if len(this_ans) != 0:
            return this_ans
        retries += 1
        print(f"running again*{retries}:", file)
    return []


def main(args):
    start = time.time()
    ans = []
    null_text = []
    my_ocr_list = get_files(args.file_path_dir, args.start_suffix, args.suffix, args.go_over_dir)
    print(my_ocr_list)

    # 使用线程池执行并发任务
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_file, file, args.max_retries): file for file in my_ocr_list}
        for future in concurrent.futures.as_completed(futures):
            file = futures[future]  # 获取对应的文件名
            this_ans = future.result()
            if len(this_ans) != 0:
                ans.extend(this_ans)
                print(this_ans)
            else:
                null_text.append(file)
                print(null_text)

    get_or_create_directory(args.generate_file)
    # 写入json
    with open(f'{args.generate_file}.json', 'w', encoding='utf-8') as file:
        json.dump(ans, file, ensure_ascii=False, indent=4)
    # 写入CSV
    with open(f'{args.generate_file}.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['instruction', 'output'])
        for item in ans:
            writer.writerow([item['instruction'], item['output']])

    if len(null_text) > 0:
        print(null_text)
    end = time.time()
    print('\ncost:', end - start)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process OCR outputs and generate QA files.')
    parser.add_argument('--file_path_dir', type=str, default=r'D:\aProject\py\myDeepdoc\ocr_outputs',
                        help='Directory path for OCR outputs')
    parser.add_argument('--start_suffix', type=str, default='火炬电子书-2023',
                        help='Start suffix for files')
    parser.add_argument('--suffix', type=str, default='.txt', help='File suffix')
    parser.add_argument('--generate_file', type=str, required=True, default='2023QA',
                        help='Base name for generated files')
    parser.add_argument('--go_over_dir', type=bool, default=False, help='Flag to go over directory')
    parser.add_argument('--max_retries', type=int, default=3, help='retries')
    """
    conda activate myLLM_WEBUI
    python rag_stuff/getQAs.py --start_suffix 火炬电子书-2023 --generate_file rag_stuff/2023QA
    """
    args = parser.parse_args()
    main(args)
