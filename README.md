### LLM-EASY-WEBUI

mainly for llama3

### 来一个测试环境

```shell
pip freeze > requirements.txt
conda create -n myLLM_WEBUI python=3.11
conda activate myLLM_WEBUI
pip install -r requirements.txt --proxy=127.0.0.1:10809
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

### docker install

```shell
git clone https://github.com/aceliuchanghong/LLM-EASY-WEBUI.git
cd LLM-EASY-WEBUI
docker build -t LLMWebUI . --build-arg DEEPINFRA_API_KEY=my_secret_key
docker run -d --name LLMWebUI -p 80:80 LLMWebUI
```

### 虚拟环境启动jupyter

```shell
jupyter notebook 
```

### *Star History*

![Star History Chart](https://api.star-history.com/svg?repos=aceliuchanghong/LLM-EASY-WEBUI&type=Date)
