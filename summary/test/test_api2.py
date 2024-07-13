import requests
import time
import concurrent.futures


def test_media_endpoint():
    url3 = "http://112.48.199.7:8083/video"
    path5= r'C:\Users\liuch\AppData\Roaming\Tencent\WXWork\wwmapp\userdata\MeetingRecords\2024-07-12 14.06.15 刘昌洪预定的会议 378308882\meeting_02.mp4'
    need_spk = True
    file_path = path5
    try:
        files = [('files', ('test_video.mp4', open(file_path, 'rb'), 'video/mp4'))]
        # files = [('files', ('00.wav', open(path3, 'rb'), 'media/wav'))]
        # files = [('files', ('00.m4a', open(path5, 'rb'), 'media/m4a'))]
        data = {
            'initial_prompt': '会议',
            'mode': 'normal',
            'need_spk': need_spk
        }
        response = requests.post(url3, files=files, data=data)
        if response.status_code == 200:
            for i in response.json()['information']:
                print(i)
        else:
            print("Error:", response.text, response.status_code)
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except requests.exceptions.RequestException as e:
        print("Error:", e)


if __name__ == "__main__":
    start = time.time()
    num_requests = 1  # Number of concurrent requests

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(test_media_endpoint) for _ in range(num_requests)]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
                print(future.result())
            except Exception as exc:
                print(f"Generated an exception: {exc}")
    end = time.time()
    print('\n识别时间:', end - start)
