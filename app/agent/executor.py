# app/agent/executor.py

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from app.core.llm_factory import get_llm
from app.agent.tools import knowledge_base_tool, internet_search_tool
from app.core.security import is_dangerous_query


_agent_executor = None


def get_agent_executor():

    global _agent_executor
    if _agent_executor is not None:
        print("使用已缓存的agent执行器")
        return _agent_executor

    print("创建新的agent执行器")
    llm = get_llm()
    tools = [knowledge_base_tool, internet_search_tool]  # 定义工具箱
    # 定义提示词
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是一个高级企业智能助手。你拥有查询内部知识库和联网搜索的能力。"
                "请根据用户的提问，自动判断应该使用哪个工具。"
                "优先使用内部知识库回答问题，只有内部知识库无法回答时才使用联网搜索。"
                "对于创造性任务（如写诗、写邮件、翻译），请**不要**使用任何工具，直接由你自己生成。"
                "如果问题很简单（如打招呼），直接回答即可。"
                "不要泄露工具内部实现",
            ),
            ("user", "{input}"),
            (
                "placeholder",
                "{agent_scratchpad}",
            ),  # 这是一个占位符，存放 Agent 的思考过程
        ]
    )

    # 创建 Agent (使用 Tool Calling 模式，这是目前最稳定的模式)
    agent = create_tool_calling_agent(llm, tools, prompt)

    # 创建执行器 (Executor 负责运行 Agent)
    executor = AgentExecutor(
        agent=agent, tools=tools, verbose=True
    )  # verbose=True 可以看到思考过程 方便调试 能看到工具调用
    return executor


def run_agent(query: str):
    """
    对外暴露的统一接口：包含安全检查 + Agent 执行
    """
    # 第一层：安全检查
    if is_dangerous_query(query):
        return "🚫 安全拦截：检测到非法指令或潜在的prompt注入攻击，操作已拒绝。"

    # 第二层：Agent 执行
    executor = get_agent_executor()

    try:
        result = executor.invoke({"input": query})
    except Exception as e:
        return f"agent 请求处理失败，错误信息：{e}"

    return result["output"]
