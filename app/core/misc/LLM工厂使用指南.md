# LLM 工厂使用指南（混合模式）

## 🎯 优化内容

### ✅ 已完成的优化

1. **去掉了 Optional 类型提示** - 代码更简洁清爽
2. **支持两个参数** - `temperature` 和 `model_name` 都可以传入
3. **实现混合模式** - 平衡性能和灵活性

---

## 🚀 三种使用模式

### 模式 1️⃣：默认单例（最常用）

```python
from app.core.llm_factory import get_llm

# 使用配置文件的默认参数
llm = get_llm()
response = llm.invoke("你好")
```

**特点：**
- ✅ 只创建一次，性能最优
- ✅ 自动使用配置文件的参数
- ✅ 适合 90% 的场景

---

### 模式 2️⃣：自定义参数缓存（推荐）

```python
from app.core.llm_factory import get_llm

# 创造性回答
creative_llm = get_llm(temperature=0.9)
answer1 = creative_llm.invoke("写一首诗")

# 再次使用相同参数（直接返回缓存）
creative_llm2 = get_llm(temperature=0.9)
# creative_llm2 is creative_llm → True

# 精确回答（创建新实例并缓存）
precise_llm = get_llm(temperature=0.1)
answer2 = precise_llm.invoke("1+1=?")

# 推理模型
reasoner = get_llm(model_name="deepseek-reasoner")
answer3 = reasoner.invoke("复杂推理问题")
```

**特点：**
- ✅ 相同参数只创建一次
- ✅ 不同参数自动创建新实例
- ✅ 适合需要多种配置的场景

---

### 模式 3️⃣：临时实例（不缓存）

```python
from app.core.llm_factory import get_llm

# 临时使用，不需要缓存
temp_llm = get_llm(temperature=0.5, use_cache=False)
answer = temp_llm.invoke("临时问题")

# 再次调用会创建新实例
temp_llm2 = get_llm(temperature=0.5, use_cache=False)
# temp_llm2 is temp_llm → False
```

**特点：**
- ✅ 每次都创建新实例
- ✅ 适合一次性任务
- ✅ 不占用缓存空间

---

## 📊 三种模式对比

| 模式 | 调用方式 | 缓存 | 使用场景 |
|------|---------|------|---------|
| **默认单例** | `get_llm()` | ✅ 单例 | 日常使用 |
| **自定义缓存** | `get_llm(temperature=0.9)` | ✅ 多例 | 多种配置 |
| **临时实例** | `get_llm(..., use_cache=False)` | ❌ 不缓存 | 一次性任务 |

---

## 💡 实际使用示例

### 示例 1：RAG 问答系统

```python
from app.core.llm_factory import get_llm

# 主流程用默认配置
llm = get_llm()

# 处理用户问题
user_question = "什么是机器学习？"
docs = search_knowledge_base(user_question)

# 生成回答
response = llm.invoke(f"基于文档：{docs}\n回答问题：{user_question}")
```

### 示例 2：多风格回答

```python
from app.core.llm_factory import get_llm

question = "介绍一下 Python"

# 专业风格（低温度）
professional_llm = get_llm(temperature=0.2)
answer1 = professional_llm.invoke(question)

# 创造性风格（高温度）
creative_llm = get_llm(temperature=0.9)
answer2 = creative_llm.invoke(question)

# 以后再次使用，直接从缓存获取
# professional_llm2 = get_llm(temperature=0.2)  # 直接返回缓存
```

### 示例 3：Agent 场景

```python
from app.core.llm_factory import get_llm

# Agent 主循环用默认配置
agent_llm = get_llm()

# 工具调用
tools = [search_tool, calculator_tool]
agent = create_agent(agent_llm, tools)

# 执行任务
result = agent.run("帮我搜索并总结...")
```

---

## 🔍 调试功能

### 查看缓存状态

```python
from app.core.llm_factory import LLMFactory

# 查看当前缓存了哪些实例
cache_info = LLMFactory.get_cache_info()
print(cache_info)

# 输出示例：
# {
#     'default_instance': True,
#     'custom_instances_count': 2,
#     'custom_configs': [
#         ('deepseek-chat', 0.9),
#         ('deepseek-chat', 0.1)
#     ]
# }
```

### 重置缓存（测试用）

```python
from app.core.llm_factory import LLMFactory

# 清空所有缓存
LLMFactory.reset()

# 重新创建
llm = get_llm()  # 会重新初始化
```

---

## ⚡ 性能说明

### 创建开销

```
创建一个 ChatOpenAI 实例：<0.001秒
调用一次 API：1-2秒

结论：创建实例的开销可以忽略不计
```

### 内存占用

```
一个 ChatOpenAI 实例：约 5KB
创建 100 个实例：约 500KB（完全可接受）

结论：除非创建上千个实例，否则内存占用可忽略
```

### 缓存收益

```
相同参数频繁调用：
- 无缓存：每次创建 0.001秒 × 1000次 = 1秒
- 有缓存：创建一次 0.001秒 + 查询999次 = 0.001秒

收益：节省 ~1秒（适合高频调用场景）
```

---

## 🎓 设计思想

### 为什么要混合模式？

1. **默认单例**：大部分场景用默认配置，单例最省资源
2. **自定义缓存**：偶尔需要不同配置，缓存避免重复创建
3. **不缓存选项**：提供最大灵活性

### 为什么去掉 Optional？

```python
# 之前：类型提示太复杂
def get_llm(temperature: Optional[float] = None) -> ChatOpenAI:
    pass

# 现在：简洁清爽
def get_llm(temperature=None, model_name=None, use_cache=True):
    pass
```

**原因：**
- Python 是动态类型语言，类型提示是可选的
- 对于学习项目，简洁性 > 严格性
- IDE 依然能提供智能提示

---

## 📝 总结

| 优化项 | 优化前 | 优化后 |
|--------|--------|--------|
| **类型提示** | 复杂（Optional） | 简洁（无类型） |
| **参数支持** | 只有 temperature | temperature + model_name |
| **模式** | 单一单例 | 混合模式（3种） |
| **灵活性** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **性能** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **代码复杂度** | 简单 | 适中 |

**建议：**
- 日常使用：`get_llm()`
- 需要调整：`get_llm(temperature=0.9)`
- 临时任务：`get_llm(..., use_cache=False)`

---

## 🚀 下一步

优化完成后，你可以：

1. ✅ 继续学习 RAG 模块
2. ✅ 继续学习 Agent 模块
3. ✅ 随时回来调整 LLM 配置

**工厂已经优化完毕，可以专注于核心功能开发了！** 🎉

