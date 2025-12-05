# 实现 RAG 链
# 这里没有使用 LangChain 的 RetrievalQA  是因为LCEL (LangChain Expression Language) 方式更灵活 可以自定义prompt

import sys
from pathlib import Path

root_location = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_location))


from langchain_core.prompts import (
    ChatPromptTemplate,
)  # 拼 prompt 的模板工具  把 {context}、{question} 这种占位符替换成真正的文本，生成要给 LLM 的消息列表。
from langchain_core.output_parsers import (
    StrOutputParser,
)  # 把 LLM 返回的对象，变成纯字符串 因为模型返回的是 AIMessage 之类的对象，不是 str
from langchain_core.runnables import (
    RunnablePassthrough,
)  # 什么都不干，原样把输入传下去 不做任何处理
from app.core.llm_factory import get_llm
from app.rag.vector_store import load_vector_store, search

# 在这里使用输出相似度分数的搜索好像没什么用 因为最后还是要用format_docs拼接成一个长字符串
# 而且最后ai的回答也不需要相似度分数

_cached_chain = None
# 定义一个全局变量 缓存链（链包括知识库、检索器、提示词、LLM）


def format_docs(docs):
    return "\n\n".join(
        f"文档来源：{d.metadata}\n文档内容：{d.page_content}" for d in docs
    )


def get_rag_chain():

    global _cached_chain
    if _cached_chain is not None:
        print("使用已缓存的RAG链")
        return _cached_chain

    print("创建新的RAG链")
    vectorstore = load_vector_store()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    template = """你是一个专业的企业知识库助手。请严格根据以下的【上下文信息】回答用户的问题。
    
    规则：
    1. 如果【上下文信息】中包含了答案，请用通俗易懂的语言回答。
    2. 如果【上下文信息】中没有相关信息，请直接回答“我的知识库中没有关于这个问题的记录”，不要编造答案。
    3. 并注明参考来源。

    【上下文信息】：
    {context}

    【用户问题】：
    {question}

    回答："""

    prompt = ChatPromptTemplate.from_template(template)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | get_llm()
        | StrOutputParser()
    )
    _cached_chain = rag_chain
    print("RAG链创建完成并缓存")
    return _cached_chain


def answer_with_knowledge_base(question: str) -> str:
    rag_chain = get_rag_chain()
    return rag_chain.invoke(question)


if __name__ == "__main__":

    while True:
        q = input("请输入您的问题:(输入q退出)")
        if q.lower() == "q":
            break
        answer = answer_with_knowledge_base(q)
        print(f"回答：{answer}")
