# 先把main里面的启动给注释掉
# 指定基础镜像
FROM python:3.11

# 指定镜像内的工作目录
WORKDIR /code

# 从本地源路径中复制requirements文件到目标路径中，注意这里仅复制了这个文件，是为了使得接着构建的镜像能够利用缓存；因为依赖包通常不频繁发生改动，所以先把它构建了。
COPY ./requirements.txt /code/requirements.txt

# 执行命令，这里是安装依赖包。
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 再复制其余的源文件，这些源文件因为是业务逻辑，所以变动的可能性很大，放在最上面构建，而不是放在最开头构建，能够有效地避免这一部分带来的变化，从而利用缓存，节省构建时间。
COPY . /code

# 让端口可用于外界访问
EXPOSE 80

# 定义环境变量
ARG DEEPINFRA_API_KEY
ENV DEEPINFRA_API_KEY=$DEEPINFRA_API_KEY

# 在容器启动时运行Python脚本
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
