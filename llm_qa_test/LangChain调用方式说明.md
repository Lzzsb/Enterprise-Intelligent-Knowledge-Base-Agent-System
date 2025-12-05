# LangChain 调用 LLM 的方式详解

**正常调用大模型需要传入 system 和 user，为什么 LangChain 只传一个字符串？**
## 📖 答案
LangChain 提供了**多层次的封装**，从最简单到最灵活，你可以根据需求选择：

---

## 三种调用方式对比

### 方式 1️⃣：最简单（字符串）

```python
response = llm.invoke("你好，请介绍你自己")
```

**等价于原生 API：**
```python
messages = [
    {"role": "user", "content": "你好，请介绍你自己"}
]
# 注意：没有 system 消息！
```

**适用场景：**
- 快速测试
- 不需要特定角色设定
- 简单的一问一答

---

### 方式 2️⃣：完整控制（LangChain Message 对象）

```python
from langchain.schema import SystemMessage, HumanMessage

messages = [
    SystemMessage(content="你是一个Python专家"),
    HumanMessage(content="请介绍你自己")
]
response = llm.invoke(messages)
```

**等价于原生 API：**
```python
messages = [
    {"role": "system", "content": "你是一个Python专家"},
    {"role": "user", "content": "请介绍你自己"}
]
```

**适用场景：**
- 需要设定 AI 的角色和行为
- 更精准的控制回答风格
- **我们的项目会主要用这种方式**

---

### 方式 3️⃣：字典格式（最接近原生 API）

```python
messages = [
    {"role": "system", "content": "你是一个幽默的助手"},
    {"role": "user", "content": "请介绍你自己"}
]
response = llm.invoke(messages)
```

**就是原生 API 的格式！**

**适用场景：**
- 从原生 API 迁移到 LangChain
- 需要兼容旧代码
- 习惯原生格式

---

## 🎯 System Prompt 的重要性

### 为什么需要 System Prompt？

```python
# ❌ 没有 system prompt
response = llm.invoke("什么是 Python 装饰器？")
# 可能回答：Python装饰器是一种设计模式...（比较笼统）

# ✅ 有 system prompt
messages = [
    SystemMessage(content="你是一个给初学者讲解的Python老师，用简单的比喻和例子"),
    HumanMessage(content="什么是 Python 装饰器？")
]
response = llm.invoke(messages)
# 会回答：想象装饰器是给函数穿衣服...（更适合初学者）
```

**System Prompt 控制：**
- 🎭 角色定位（专家/老师/助手）
- 🗣️ 回答风格（专业/幽默/简洁）
- 📏 回答长度和格式
- 🎯 任务类型（翻译/总结/代码）

---

## 💡 在我们项目中的应用

### RAG 场景（知识库问答）

```python
system_prompt = """
你是一个企业知识库助手。
你的任务是基于给定的文档片段回答用户问题。
如果文档中没有相关信息，明确告诉用户"文档中未找到相关信息"。
不要编造答案。
"""

messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content=f"文档内容：{retrieved_docs}\n\n用户问题：{user_question}")
]
```

### Agent 场景（工具调用）

```python
system_prompt = """
你是一个智能助手，可以使用工具帮助用户。
可用工具：
1. search_kb - 搜索知识库
2. web_search - 网络搜索
3. calculator - 计算器

思考步骤：
1. 理解用户需求
2. 选择合适的工具
3. 整合结果回答
"""
```

---

## 🧪 运行更新后的测试

现在运行 `test_llm.py`，你会看到三种方式的对比！

```bash
python test_llm.py
```

你会注意到：**同样的问题，加了 system prompt 后，回答的风格和内容会不同！**

---

## 📝 练习建议

试试修改 `test_llm.py` 中的 system prompt：

1. **专业风格：** "你是一个严肃的技术专家，回答要专业准确。"
2. **幽默风格：** "你是一个幽默风趣的AI，喜欢用段子和比喻。"
3. **简洁风格：** "你的回答必须控制在20字以内。"

看看回答有什么不同！

---

## ✅ 总结

| 特性 | 方式1（字符串） | 方式2（Message对象） | 方式3（字典） |
|------|----------------|---------------------|--------------|
| 简洁度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 灵活度 | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| System Prompt | ❌ 不支持 | ✅ 支持 | ✅ 支持 |
| 推荐场景 | 快速测试 | **生产环境** | API迁移 |

**我们项目主要用方式2！** 🎯

