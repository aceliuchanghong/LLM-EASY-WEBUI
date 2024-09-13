import requests
import time
import json


def test_clone_voice_endpoint():
    base = "http://192.168.149.42:11796"
    url3 = "http://192.168.149.42:11796/process_audio/"
    path3 = r'C:\Users\liuch\Music\ylhtest.wav'
    file_path = path3
    try:
        with open(file_path, 'rb') as f:
            file = {'file': ('post.wav', f, 'media/wav')}
            data = {
                'apiKey': 'application-e136b55b610a188f23d253349af9509f',
            }
            response = requests.post(url3, files=file, params=data, stream=True)
            if response.status_code == 200:
                for i in response:
                    str_i = i.decode('utf-8')
                    # 将字符串转换成字典
                    data = json.loads(str_i)
                    if data.get('result', None) is not None:
                        # 提取result的值
                        result = base + data.get('result', None)
                        print(result)
            else:
                print("Error:", response.text, response.status_code)
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except requests.exceptions.RequestException as e:
        print("Error:", e)


if __name__ == "__main__":
    start = time.time()
    test_clone_voice_endpoint()
    end = time.time()
    print('\n识别时间:', end - start)
