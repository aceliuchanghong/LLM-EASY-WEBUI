import requests
import time


def test_media_endpoint():
    url = "http://112.48.199.197:8083/video"
    url2 = "http://192.168.18.106:8083/video"
    path1 = r'C:\Users\liuch\Videos\test1.mp4'
    path2 = r'C:\Users\liuch\Videos\meeting_01.mp4'
    path3 = r'D:\BaiduNetdiskDownload\15.wav'
    try:
        files = [('files', ('test_video.mp4', open(path1, 'rb'), 'video/mp4'))]
        # files = [('files', ('00.wav', open(path3, 'rb'), 'media/wav'))]
        data = {
            'initial_prompt': '会议',
            'mode': 'timeline'
        }
        response = requests.post(url2, files=files, data=data)
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
