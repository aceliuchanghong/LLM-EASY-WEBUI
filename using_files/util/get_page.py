import requests


def fetch_url_content(target_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    url = "https://r.jina.ai/" + target_url
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: Unable to fetch content. Status code: {response.status_code}"


target_url = "https://python.langchain.com/v0.1/docs/integrations/vectorstores/milvus/"
content = fetch_url_content(target_url)
print(content)
# 打印响应内容
# with open("example.md", "w", encoding="utf-8") as file:
#     file.write(content)
