### 结构

```text
summary/
|
├── config.py
├── readme.md
├── mp4_sum/
│   ├── allSummaryWorker.py
│   ├── core.py
│   └── stepSummaryWorker.py
├── text_sum/
│   ├── allSummaryWorker.py
│   └── core.py
├── util/
│   ├── check_db.py
│   ├── create_llm.py
│   ├── mp3_from_mp4.py
│   ├── text_from_file.py
│   └── text_from_mp3.py
└── worker/
    └── Worker.py
```

测试执行语句,真正执行的时候做一个循环执行

```shell
# 环境安装配置
git clone https://github.com/aceliuchanghong/LLM-EASY-WEBUI.git
# 配置好环境变量OPENAI_API_KEY,配置好需要的pthon虚拟环境(参见项目readme)
# 我已经做好了,只需要激活就好了
source activate mySummary
cd LLM-EASY-WEBUI
pip install -r requirements.txt
""" 报错忽略
ERROR: Could not find a version that satisfies the requirement pywin32==306 (from versions: none)
ERROR: No matching distribution found for pywin32==306
pip install langchain-openai
pip install easy-media-utils
"""

参数简短说明:
# SumMp4All,SumTextAll==>总体总结 SumMp4Step==>章节总结  
# summary/config.py里面有一个音频模型文件需要下载好,修改model_size_or_path的路径(/home/liuchanghong/faster-whisper-large-v3)
# 重跑的话增加 --reRun
```

测试语句

```shell
# 本机测试语句
python .\smain.py --summaryType SumMp4All --filePath "C:\Users\lawrence\Videos\yunyin.mp4" --fileInfo "说剑"
python .\smain.py --summaryType SumMp4Step --filePath "C:\Users\lawrence\Videos\yunyin.mp4" --fileInfo "说剑"
python .\smain.py --summaryType SumTextAll --filePath "C:\Users\lawrence\Videos\XX.pdf" --fileInfo "说剑"
python .\smain.py --summaryType SumMp4Step --filePath "C:\Users\lawrence\Videos\yunyin.mp4" --fileInfo "说剑" --reRun

# 服务器测试语句
# 测试视频 
wget http://flv4mp4.people.com.cn/videofile7/pvmsvideo/2024/4/30/RenMinShiPinBianJiZu-QinRong_4a7019afadf230e3364df531ec39dbed_android_c.mp4
cd /home/liuchanghong/LLM-EASY-WEBUI
python smain.py --summaryType SumMp4Step --filePath "/home/liuchanghong/LLM-EASY-WEBUI/summary/test/waijiaobu.mp4" --fileInfo "中国外交部发言"
python smain.py --summaryType SumMp4All --filePath "/home/liuchanghong/LLM-EASY-WEBUI/summary/test/waijiaobu.mp4" --fileInfo "中国外交部发言"
```

TODO

- 增加docx,doc,excel,pdf,txt文件总结
- 增加webui界面
