### 结构

```text
summary/
|
├── ui.py                       *************** UI入口
├── smain.py                    *************** cli入口
├── config.py                   *************** 配置属性
├── media_sum.db                *************** 数据库
├── readme.md
├── mp4_sum/
│   ├── allSummaryWorker.py     *************** 继承core,实现总体总结
│   ├── core.py                 *************** 继承Worker,媒体总结抽象大类
│   └── stepSummaryWorker.py    *************** 继承core,实现分步总结
├── util/
│   ├── check_db.py             *************** 数据库工具函数
│   ├── create_llm.py           *************** 大模型工具函数
│   ├── mp3_from_mp4.py         *************** 媒体文件处理工具函数
│   ├── speaker_recognition.py  *************** 没实现的分人物说话的工具函数
│   └── text_from_mp3.py        *************** 工具函数
└── worker/
    └── Worker.py               *************** 根节点抽象类
```

```text
腾讯会议总结模板
录制文件：https://meeting.tencent.com/v2/cloud-record/share?id=1e08928b-a218-4091-8615-1d7fe5545020&from=3&record_type=2
```

```shell
# 环境安装配置
git clone https://github.com/aceliuchanghong/LLM-EASY-WEBUI.git
# 配置好环境变量OPENAI_API_KEY(或者不用直接修改配置的apiKey),配置好需要的python虚拟环境(参见项目readme)
# 我已经做好了,只需要激活就好了
source activate myLLM_WEBUI
cd LLM-EASY-WEBUI
pip install -r requirements.txt

# 修改summary/config.py:
# 有一个音频模型文件需要提前下载好,修改model_size_or_path的路径(参考:/home/liuchanghong/faster-whisper-large-v3)
# file_default_path这个是指自己传的文件路径,记得改 (参考:/home/liuchanghong/media_files)
# 参考修改 db_path = "/home/liuchanghong/media_files/media_sum.db"

# 找个目录下载
wget https://github.com/Purfview/whisper-standalone-win/releases/download/libs/cuBLAS.and.cuDNN_CUDA11_linux_v4.7z
7za x cuBLAS.and.cuDNN_CUDA11_linux_v4.7z
# 把 上面解压获得的 *.so.* 放置到虚拟环境的lib下面,或者其他path都可以
cp /home/liuchanghong/faster-whisper-large-v3/*.so.* $HOME/anaconda3/envs/mySummary/lib
# 以下六个文件 libcublasLt.so.12,libcublasLt.so.11 && libcublasLt.so.11,libcublasLt.so.12其实一样的,只是名字我改了
#-rw-rw-r--  1 liuchanghong liuchanghong 574565016 May  5 07:41 libcublasLt.so.12
#-rw-rw-r--  1 liuchanghong liuchanghong  94729912 May  5 07:41 libcublas.so.12
#-rw-rw-r--  1 liuchanghong liuchanghong 574565016 May  5 08:21 libcublasLt.so.11
#-rw-rw-r--  1 liuchanghong liuchanghong  94729912 May  5 08:21 libcublas.so.11
#-rw-rw-r--  1 liuchanghong liuchanghong 563283840 May  5 08:21 libcudnn_cnn_infer.so.8
#-rw-rw-r--  1 liuchanghong liuchanghong  90849728 May  5 08:21 libcudnn_ops_infer.so.8

## 报错忽略
## ERROR: Could not find a version that satisfies the requirement pywin32==306 (from versions: none)
## ERROR: No matching distribution found for pywin32==306
## 执行时候报错缺少模块,就安装就好了
## pip install langchain-openai
## pip install easy-media-utils
## pip install moviepy
## pip install gradio

参数简短说明:
# summaryType:SumMp4All,SumTextAll==>总体总结 SumMp4Step==>章节总结  
# fileInfo==>视频说明,不是关键字
# vi summary/config.py
# 有一个音频模型文件需要提前下载好(hf的faster-whisper-large-v3),模型地址:model_size_or_path
# file_default_path这个是指自己上传的文件路径,记得改 (/home/liuchanghong/media_files)
# 如果使用的官方key,里面openai_api_base记得改下(模型也可以改一下) 
# db_path 数据库地址
```

测试执行语句,真正执行的时候做一个循环执行

```shell
# UI界面,不要传大视频,真的会卡掉的,掉了需要重拉,记得开端口
nohup uvicorn ui:app --port 9898 --host 0.0.0.0> unicore.log &
(uvicorn ui:app --port 9898 --host 0.0.0.0)
# 或者
python ui.py

# 本机测试语句 重跑的话增加 --reRun
python .\smain.py --summaryType SumMp4All --filePath "C:\Users\lawrence\Videos\yunyin.mp4" --fileInfo "说剑"
python .\smain.py --summaryType SumMp4Step --filePath "C:\Users\lawrence\Videos\yunyin.mp4" --fileInfo "说剑"
python .\smain.py --summaryType SumTextAll --filePath "C:\Users\lawrence\Videos\XX.pdf" --fileInfo "说剑"
python .\smain.py --summaryType SumMp4Step --filePath "C:\Users\lawrence\Videos\yunyin.mp4" --fileInfo "天子之剑，以燕溪石城为锋，齐岱为锷，晋魏为脊，周宋为镡，韩魏为夹" --reRun
python .\smain.py --summaryType SumMp4All --filePath "C:\Users\lawrence\Videos\yunyin.mp4" --fileInfo "天子之剑，以燕溪石城为锋，齐岱为锷，晋魏为脊，周宋为镡，韩魏为夹" --reRun
python .\smain.py --summaryType SumMp4All --filePath "C:\Users\lawrence\Videos\waijiaobu.mp4" --fileInfo "中国外交部发言"

# 服务器测试语句
# 测试视频 (由于myLLM_WEBUI放在了liuchanghong用户下,最好切换一下用户,或者自己的虚拟环境)
source activate myLLM_WEBUI
# 我测试下载的视频,改了一个名字==>waijiaobu 视频名字需要有正确含义
# wget http://flv4mp4.people.com.cn/videofile7/pvmsvideo/2024/4/30/RenMinShiPinBianJiZu-QinRong_4a7019afadf230e3364df531ec39dbed_android_c.mp4
cd /home/liuchanghong/LLM-EASY-WEBUI
python smain.py --summaryType SumMp4Step --filePath "/home/liuchanghong/LLM-EASY-WEBUI/summary/test/waijiaobu.mp4" --fileInfo "中国外交部发言"
python smain.py --summaryType SumMp4All --filePath "/home/liuchanghong/LLM-EASY-WEBUI/summary/test/waijiaobu.mp4" --fileInfo "中国外交部发言"
python smain.py --summaryType SumMp4Step --filePath "/home/liuchanghong/LLM-EASY-WEBUI/summary/test/waijiaobu.mp4" --fileInfo "中国外交部发言" --reRun

# 建议测试这2个,我只跑了这2个
python smain.py --summaryType SumMp4Step --filePath "/home/liuchanghong/media_files/企业文化讲解1.mp4" --fileInfo "格莱美企业文化宣讲"
python smain.py --summaryType SumMp4All --filePath "/home/liuchanghong/media_files/企业文化讲解1.mp4" --fileInfo "格莱美企业文化宣讲"
# 这几个更是重量级,一个比一个大,可以输出文本,但是我们使用的openai的key限制4096了,所以做了文本长度限制,可能总结不全
python smain.py --summaryType SumMp4Step --filePath "/home/liuchanghong/media_files/企业文化整体.mp4" --fileInfo "格莱美企业文化宣讲"
python smain.py --summaryType SumMp4Step --filePath "/home/liuchanghong/media_files/企业文化课程讲解1.mp4" --fileInfo "格莱美企业文化宣讲"
python smain.py --summaryType SumMp4Step --filePath "/home/liuchanghong/media_files/企业文化课程讲解2.mp4" --fileInfo "格莱美企业文化宣讲"
python smain.py --summaryType SumMp4Step --filePath "/home/liuchanghong/media_files/企业文化课程讲解3.mp4" --fileInfo "格莱美企业文化宣讲"
python smain.py --summaryType SumMp4Step --filePath "/home/liuchanghong/media_files/企业文化课程讲解4.mp4" --fileInfo "格莱美企业文化宣讲"
python smain.py --summaryType SumMp4Step --filePath "/home/liuchanghong/media_files/企业文化课程讲解5.mp4" --fileInfo "格莱美企业文化宣讲"
```

TODO

- 增加docx,doc,excel,pdf,txt文件总结
- 分人物说话
- 对录音文件,做rag
