### LLM-EASY-WEBUI

mainly for llama3

### 来一个测试环境

```shell
pip freeze > requirements.txt
conda create -n myLLM_WEBUI python=3.11
conda activate myLLM_WEBUI
pip install -r requirements.txt --proxy=127.0.0.1:10809
watch -n 1 nvidia-smi
nvitop
```

### Structure

```text
LLM-EASY-WEBUI/
|
├── config.py
├── main.py
├── sUI.py
├── smain.py
└── ui.py
```
### start

```shell
git clone https://github.com/aceliuchanghong/LLM-EASY-WEBUI.git
cd LLM-EASY-WEBUI
source activate llm_uncensor
pip install -r requirements.txt
vi chatAll/config.py

查看(sudo lsof -i :11434)
LLM_MODEL_NAME = 'wangrongsheng/mistral-7b-v0.3-chinese-chat:latest'
LLM_BASE_URL = 'http://127.0.0.1:11434/v1/'
DEEPINFRA_API_KEY = 'wangrongsheng/mistral-7b-v0.3-chinese-chat:latest'
EMBEDDING_MODEL = 'BAAI/bge-large-en-v1.5'
file_default_path = '/home/administrator/ollama/LLM-EASY-WEBUI'
# 删除这2行
pywin32==306
pywinpty==2.0.13
```

### 虚拟环境启动jupyter

```shell
jupyter notebook 
```

### *Star History*

![Star History Chart](https://api.star-history.com/svg?repos=aceliuchanghong/LLM-EASY-WEBUI&type=Date)
