# 企业级智能知识库问答系统（RAG + Agent）

一个基于 **LangChain + FastAPI + Streamlit** 的企业级私有知识库与智能体（Agent）解决方案，支持文档上传、向量检索问答、工具调用、防提示注入等工程化能力。

---

## ✨ 功能特性
- 📄 **RAG 检索问答**：支持 PDF/TXT/MD 文档加载、切分、向量化（FAISS），基于私有知识库精准回答。
- 🧠 **LLM 工厂**：统一的 LLM 初始化与单例管理（支持自定义 temperature / model）。
- 🔎 **向量存储**：FAISS 本地向量库，支持保存/加载、相似度搜索与得分返回。
- 🛡️ **安全防护**：设计并实现了应用层安全护栏模块，对用户 Query 进行启发式安全检测（Prompt Injection、System Prompt Exfiltration、危险命令注入等），采用规则分级 + 风险聚合的方式输出结构化安全结果，并通过日志系统记录安全事件，可作为后续审计与风控策略的基础
- 🧰 **Agent 工具**：可扩展工具调用（搜索、计算等），支持 LangChain Agent 流程。
- 🖥️ **API + UI**：FastAPI 提供接口，Streamlit 提供简易 Web UI。
- 🐳 **容器化**：可通过 Docker / Compose 部署。

---

## 📂 项目结构
```
enterprise_agent/
├── app/
│   ├── main.py                 # FastAPI 入口
│   ├── core/                   # 核心：配置、LLM/Embedding 工厂、安全
│   ├── rag/                    # RAG：加载、切分、向量库、RAG 链
│   ├── agent/                  # Agent：工具与执行器
│   └── api/                    # API：V1 路由与 schemas
├── docs/                       # 示例文档
├── ui/                         # Streamlit 前端
├── requirements.txt            # 依赖列表
├── .env.example                # 环境变量样例
└── vector_store_here/          # 示例向量库（演示用，可删除）
```

---

## 🔧 环境与依赖
1) **Python 3.10+**
2) 推荐创建虚拟环境
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# 或 source venv/bin/activate  # macOS/Linux
```
3) 安装依赖
```bash
pip install -r requirements.txt
```

---

## ⚙️ 环境变量（.env）
复制 `.env.example` 到 `.env` 并填写（至少以下三项）：
```
LLM_API_KEY=your_api_key_here
LLM_API_BASE_URL=https://api.deepseek.com
LLM_MODEL_NAME=deepseek-chat
# 可选：LLM_TEMPERATURE=0.7
# 可选：VECTOR_STORE_PATH=./vector_store_here
```

---

## 🚀 快速运行
### 后端 API（FastAPI）
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
接口示例：
- `GET /` 健康检查
- `POST /api/v1/chat`  聊天/问答

### 前端 UI（Streamlit）
```bash
cd ui
streamlit run app.py --server.port 8501
```
在浏览器访问：`http://localhost:8501`

---

## 🧪 本地测试（示例）
在项目根目录运行：
```bash
# 测试向量存储流程（需先准备 docs/ 下的示例文档）
python app/rag/misc/test_vector_store.py

# 测试 LLM 工厂
python app/core/misc/test_llm_factory.py
```

---

## 🛠️ 开发说明
- 代码风格：PEP8 + 类型提示
- 依赖管理：`requirements.txt`
- 配置管理：`app/core/config.py`（Pydantic Settings）
- LLM/Embedding：`app/core/llm_factory.py`, `app/core/embedding_factory.py`
- RAG：`app/rag/loader.py`, `splitter.py`, `vector_store.py`
- Agent：`app/agent/tools.py`, `executor.py`

---

## 📦 Docker 部署
- 前置：准备 `.env`（包含 LLM_API_KEY / LLM_API_BASE_URL / LLM_MODEL_NAME），确认本机 8000、8501 端口空闲。
- 构建并启动（后台运行）：
```bash
docker compose up --build -d   # 后台运行
```
- 访问：
  - API: `http://localhost:8000`（Swagger: `/docs`）
  - Web UI: `http://localhost:8501`
- 日志与状态：
```bash
docker compose ps
docker compose logs -f api
docker compose logs -f web
```
- 停止并清理容器（保留向量库等挂载数据）：
```bash
docker compose down
```

---

## 📄 开源许可
本项目默认 MIT License（如有需要可自行调整）。