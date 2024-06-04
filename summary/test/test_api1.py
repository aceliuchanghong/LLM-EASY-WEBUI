import requests
import json


def test_media_endpoint():
    url = "http://112.48.199.63:9898/media"
    data = {
        "audio_path": "/mnt/data/llch/media_path/00.mp4.mp3",
        "initial_prompt": '支持小岛国迈向更具韧性的持久繁荣',
        "mode": 'timeline',
    }
    response = requests.post(url, params=data)
    if response.status_code == 200:
        print(response.json())
    else:
        print("Error:", response, response.status_code)


if __name__ == "__main__":
    test_media_endpoint()
