from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware,
)  # Cross-Origin Resource Sharing 跨域资源共享   让浏览器前端streamlit可以访问这个后端 API 便于美化
from app.api.v1.endpoints import chat

# 初始化 APP
app = FastAPI(
    title="Enterprise AI Agent API",
    description="基于 RAG + Agent 的企业级知识库助手 API",
    version="1.0.0",
)

# --- 核心配置：跨域资源共享 (CORS) ---
# 允许 Streamlit (默认端口 8501) 访问这个 API
origins = [
    "http://localhost",
    "http://localhost:8501",
    "*",  # 开发阶段允许所有来源，生产环境要改掉
]

# 添加跨域资源共享中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由router挂载在app上 可以通过http://localhost:8000/api/v1访问router
# 再加上之前挂载在router中的路由 比如/chat 就可以通过http://localhost:8000/api/v1/chat 访问
# tags=["Chat"] 是Swagger 文档里的分组标签 比如/chat 的标签是"Chaaaat"
app.include_router(chat.router, prefix="/api/v1", tags=["Chaaaat"])


# 健康检查  是直接挂载在app上的路由 而不是挂载在chat.router上的路由  可以直接通过http://localhost:8000/ 访问
@app.get("/")
def health_check():
    return {"status": "ok", "message": "Service is running 🚀"}


if __name__ == "__main__":
    import uvicorn  # 导入 Uvicorn，这是一个 ASGI 服务器 用于运行 FastAPI 应用

    # 启动服务器
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    # "app.main:app" 是 FastAPI 应用的导入路径
    # host="0.0.0.0" 是监听所有 IP 地址 这样其他电脑也可以访问这个服务器
    # port=8000 是监听的端口
    # reload=True 是自动重新加载代码 这样每次修改代码后不需要手动重启服务器
