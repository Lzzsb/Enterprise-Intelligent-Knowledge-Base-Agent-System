# ui/app.py

import streamlit as st
import requests
import json

# 设置页面标题
st.set_page_config(page_title="企业级智能知识库助手", page_icon="🤖")

st.title("🤖 企业级 AI 智能助手 (RAG + Agent)")

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示聊天历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 聊天输入框
if prompt := st.chat_input("请输入您的问题..."):
    # 1. 显示用户输入
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. 调用FastAPI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("⏳ 思考中...")  # 显示加载状态

        try:
            # 这里的 URL 是你 FastAPI 的地址
            api_url = "http://127.0.0.1:8000/api/v1/chat"
            payload = {"query": prompt, "use_search": False}

            # 发送请求
            response = requests.post(api_url, json=payload)

            if response.status_code == 200:
                result = response.json()
                answer = result.get("answer", "出错了：没有返回答案")

                # 显示 AI 回答
                message_placeholder.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
            else:
                error_msg = f"❌ 服务器报错: {response.status_code}"
                message_placeholder.markdown(error_msg)

        except Exception as e:
            message_placeholder.markdown(f"❌ 连接 API 失败: {str(e)}")
