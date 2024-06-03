import requests


def test_chat_endpoint():
    url = "http://localhost:8000/chat"
    params = {
        "prompt": "写一首七言绝句诗"
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        print(response.json())
    else:
        print("Error:", response, response.status_code, response.text)


if __name__ == "__main__":
    test_chat_endpoint()
