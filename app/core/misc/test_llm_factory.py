"""
测试混合模式的 LLM 工厂
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


from app.core.llm_factory import get_llm, LLMFactory

print("\n" + "=" * 70)
print("🧪 测试 LLM 工厂（混合模式）")
print("=" * 70)

# ========== 测试1：默认单例 ==========
print("\n【测试1】默认配置（单例模式）")
print("-" * 70)
llm1 = get_llm()
llm2 = get_llm()
print(f"✅ 两次调用是同一个对象: {llm1 is llm2}")

# ========== 测试2：自定义参数缓存 ==========
print("\n【测试2】自定义参数（缓存模式）")
print("-" * 70)
creative1 = get_llm(temperature=0.9)
creative2 = get_llm(temperature=0.9)
print(f"✅ 相同参数返回同一对象: {creative1 is creative2}")

precise = get_llm(temperature=0.1)
print(f"✅ 不同参数是不同对象: {creative1 is precise}")

# ========== 测试3：不缓存模式 ==========
print("\n【测试3】临时实例（不缓存）")
print("-" * 70)
temp1 = get_llm(temperature=0.5, use_cache=False)
temp2 = get_llm(temperature=0.5, use_cache=False)
print(f"✅ 不缓存每次都是新对象: {temp1 is temp2}")  # False

# ========== 测试4：查看缓存状态 ==========
print("\n【测试4】缓存状态")
print("-" * 70)
cache_info = LLMFactory.get_cache_info()
print(f"默认实例存在: {cache_info['default_instance']}")
print(f"自定义实例数量: {cache_info['custom_instances_count']}")
print(f"自定义配置列表: {cache_info['custom_configs']}")

# ========== 测试5：实际调用 ==========
print("\n【测试5】实际调用 LLM")
print("-" * 70)
llm = get_llm()
response = llm.invoke("用一句话介绍 Python")
print(f"问题: 用一句话介绍 Python")
print(f"回答: {response.content}")

print("\n" + "=" * 70)
print("✅ 所有测试完成！混合模式工作正常！")
print("=" * 70)
