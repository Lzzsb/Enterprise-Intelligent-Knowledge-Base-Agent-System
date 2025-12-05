"""
LangChain 调用 LLM 的三种方式演示

使用的是最小RAG pipeline
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# 加载环境变量
load_dotenv()

# 从环境变量读取配置
api_key = os.getenv("LLM_API_KEY")
api_base = os.getenv("LLM_API_BASE_URL")
model_name = os.getenv("LLM_MODEL_NAME")

# 初始化 LLM
print("\n🔧 正在初始化 LLM...")
llm = ChatOpenAI(
    model=model_name,
    openai_api_base=api_base,
    openai_api_key=api_key,
    temperature=0.7,
)
print("✅ LLM 初始化成功!\n")

print("方式1️⃣: 最简单 - 直接传字符串（只有 user 消息）")
response1 = llm.invoke("你好，请用一句话介绍你自己。")
print(f"回答: {response1.content}\n")

print("方式2️⃣: 传入消息列表（包含 system + user）")
messages = [
    SystemMessage(content="你是一个专业的Python编程助手，擅长解释技术概念。"),
    HumanMessage(content="请用一句话介绍你自己。"),
]
response2 = llm.invoke(messages)
print(f"回答: {response2.content}\n")

print("方式3️⃣: 原生风格（字典格式，更接近原生 API）")
messages_method3 = [
    {"role": "system", "content": "你是一个幽默风趣的AI助手，喜欢用比喻讲解。"},
    {"role": "user", "content": "请用一句话介绍你自己。"},
]
response3 = llm.invoke(messages_method3)
print(f"回答: {response3.content}\n")

print("💡 总结：三种方式都可以，选择最适合你的！")
