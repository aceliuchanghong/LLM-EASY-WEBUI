### 结构

```text
summary/
|
├── config.py
├── main.py
├── readme.md
├── mp4_sum/
│   ├── allSummaryWorker.py
│   ├── core.py
│   └── stepSummaryWorker.py
├── text_sum/
│   ├── allSummaryWorker.py
│   ├── core.py
│   └── stepSummaryWorker.py
├── util/
│   ├── create_llm.py
│   └── text_from_mp3.py
└── worker/
    └── Worker.py
```

测试文本

```shell
python .\smain.py --summaryType SumMp4All --filePath "C:\Users\lawrence\Videos\yunyin.mp4"
python .\smain.py --summaryType SumMp4Step --filePath "C:\Users\lawrence\Videos\yunyin.mp4"
```
