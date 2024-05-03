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
git clone https://github.com/aceliuchanghong/LLM-EASY-WEBUI.git
# SumMp4All,SumTextAll==>总体总结 SumMp4Step==>章节总结  
# 配置好环境变量OPENAI_API_KEY,配置好需要的pthon虚拟环境(参见项目readme)
# summary/config.py里面有一个音频模型文件需要下载好,修改model_size_or_path的路径
# 重跑的话增加 --reRun
```

```shell

python .\smain.py --summaryType SumMp4All --filePath "C:\Users\lawrence\Videos\yunyin.mp4" --fileInfo "说剑"
python .\smain.py --summaryType SumMp4Step --filePath "C:\Users\lawrence\Videos\yunyin.mp4" --fileInfo "说剑"
# 还没写
python .\smain.py --summaryType SumTextAll --filePath "C:\Users\lawrence\Videos\XX.pdf" --fileInfo "说剑"
python .\smain.py --summaryType SumMp4Step --filePath "C:\Users\lawrence\Videos\yunyin.mp4" --fileInfo "说剑" --reRun
```
TODO

- 增加docx,doc,excel,pdf,txt文件总结
- 增加webui界面
