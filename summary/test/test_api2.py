import requests
import time


def test_media_endpoint():
    url = "http://112.48.199.197:8083/video"
    path1 = r'C:\Users\liuch\Videos\test1.mp4'
    path2 = r'C:\Users\liuch\Videos\meeting_01.mp4'
    try:
        files = [('files', ('test_video.mp4', open(path1, 'rb'), 'video/mp4'))]
        data = {
            'initial_prompt': '会议',
            'mode': 'normal'
        }
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            for i in response.json()['information']:
                print(i)
        else:
            print("Error:", response.text, response.status_code)
    except FileNotFoundError:
        print(f"Error: The file {path1} does not exist.")
    except requests.exceptions.RequestException as e:
        print("Error:", e)


if __name__ == "__main__":
    start = time.time()
    test_media_endpoint()
    end = time.time()
    print('\n识别时间:', end - start)