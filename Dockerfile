# 1. 使用官方 Python 轻量级镜像
FROM python:3.10-slim

# 2. 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1  
# 防止 Python 生成 pyc缓存 文件
ENV PYTHONUNBUFFERED=1
# 让 Python 输出日志时 不要使用缓冲区（也就是实时输出 stdout）

# 3. 设置工作目录
WORKDIR /app

# 4. 复制依赖文件并安装 (利用缓存机制加速构建)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 5. 复制项目所有代码
COPY . .

# 6. 暴露（声明）端口  给部署的人看的 告诉别人容器内部使用哪几个端口
EXPOSE 8000
EXPOSE 8501

# 默认命令 (会被 docker-compose 覆盖) 默认使用uvicorn 启动 FastAPI 应用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]