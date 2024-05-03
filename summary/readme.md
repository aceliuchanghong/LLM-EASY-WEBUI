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
python .\smain.py --summaryType SumMp4All --filePath "C:\Users\lawrence\Videos\yunyin.mp4" --fileInfo "说剑"
python .\smain.py --summaryType SumMp4Step --filePath "C:\Users\lawrence\Videos\yunyin.mp4" --fileInfo "说剑"
python .\smain.py --summaryType SumTextAll --filePath "C:\Users\lawrence\Videos\XX.pdf" --fileInfo "说剑"
```

TODO

- 增加docx,doc,excel,pdf,txt文件总结
- 增加webui界面
