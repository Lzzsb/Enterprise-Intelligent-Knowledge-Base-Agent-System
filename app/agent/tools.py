# 定义了可以被agent调用的工具
# 知识库工具：使用知识库回答问题
# 联网搜索工具：当知识库无法覆盖或需要最新信息时，进行联网搜索

from langchain_core.tools import tool
from app.rag.ragchain_langchain import answer_with_knowledge_base
from langchain_community.tools import DuckDuckGoSearchRun

_duckduckgo_search = DuckDuckGoSearchRun()  # 提前初始化 避免每次调用都创建新的对象


@tool  # 包装成tool之后可以被agent调用
def knowledge_base_tool(question: str) -> str:
    """
    使用企业内部知识库回答问题。

    优先用于：
    - 已导入到知识库中的 PDF / 文档内容
    - 需要基于“内部知识”给出相对权威答案的场景

    内部知识库存在的文件名有: comprehensive_employee_handbook,history_of_coffee, smart_home_vacuum_manual,人工智能基础知识
    """
    return answer_with_knowledge_base(question)


@tool
def internet_search_tool(question: str) -> str:
    """
    联网搜索工具（基于 DuckDuckGo）。

    适用于：
    - 需要查询最新资讯、实时事件（如：今天的新闻、最近的政策）
    - 知识库中不存在的常识性问题
    - 与互联网公开信息相关的问题

    注意：
    - 返回结果可能包含多个来源的摘要，请综合后再回答用户。
    """
    print(f"正在使用联网搜索......请稍等...")
    try:
        raw_results = _duckduckgo_search.run(question)
        if isinstance(raw_results, str) and len(raw_results) > 1000:
            return (
                f"联网搜索结果过长（超过1000字），已截断显示: {raw_results[:1000]}..."
            )
        return raw_results
    except Exception as e:
        return f"联网搜索失败，错误信息：{e}"
