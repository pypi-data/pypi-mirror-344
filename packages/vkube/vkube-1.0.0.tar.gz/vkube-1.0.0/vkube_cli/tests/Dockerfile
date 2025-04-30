# 使用官方 Python 3.9 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录下的app.py到容器的 /app 目录
COPY app.py /app

# 容器启动时运行的命令
CMD ["python3", "app.py"]

# 暴露容器的 5000 端口
EXPOSE 5009