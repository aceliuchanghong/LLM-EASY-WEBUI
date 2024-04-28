import re


def remove_comments(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        ans = ''

        in_comment_block = False
        for line in lines:
            # 判断是否处于多行注释块中
            if in_comment_block:
                # 如果当前行结束了多行注释块
                if '"""' in line:
                    in_comment_block = False
                    # 去除多余的部分
                    line = line.split('"""', 1)[1]
                else:
                    # 如果还在多行注释块中，跳过当前行
                    continue
            else:
                # 处理单行注释
                line = re.sub(r'#.*', '', line)
                # 处理多行注释的开始
                if '"""' in line:
                    in_comment_block = True
                    line = line.split('"""', 1)[0]

            # 删除行尾的空白字符
            line = line.rstrip()
            # 如果行还有内容，打印出来
            if line:
                print(line)
                ans += line + '\n'
    return ans


if __name__ == '__main__':
    input_file = '../test/test_gradio.py'
    text = remove_comments(input_file)
    with open('../ungit/00.py', 'w', encoding='utf-8') as f:
        f.write(text)
