"""
LLM 工厂模块 - 混合模式
提供统一的 LLM 初始化接口，支持单例和多实例缓存
"""

import sys
from pathlib import Path

root_location = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_location))

from langchain_openai import ChatOpenAI
from app.core.config import get_settings


class LLMFactory:
    """
    LLM 工厂类（混合模式）
    - 默认参数：使用单例（节省资源）
    - 自定义参数：可选缓存（灵活且高效）
    """

    # 默认实例（最常用的配置）
    _default_instance = None

    # 自定义参数的实例缓存
    _custom_instances = {}

    @classmethod
    def get_llm(cls, temperature=None, model_name=None, use_cache=True):
        """
        获取 LLM 实例

        参数:
            temperature: 温度参数（0-1），None则使用配置文件
            model_name: 模型名称，None则使用配置文件
            use_cache: 是否缓存实例（默认True）

        返回:
            ChatOpenAI 实例

        使用示例:
            # 使用默认配置（单例）
            llm = get_llm()

            # 自定义参数（缓存）
            creative_llm = get_llm(temperature=0.9)

            # 临时使用（不缓存）
            temp_llm = get_llm(temperature=0.5, use_cache=False)
        """
        settings = get_settings()

        # 如果使用默认参数，返回单例
        if temperature is None and model_name is None:
            if cls._default_instance is None:
                print("🏗️ 创建默认 LLM 实例（单例）")
                cls._default_instance = cls._create_llm(
                    settings.LLM_MODEL_NAME, settings.LLM_TEMPERATURE
                )
            else:
                print("♻️ 使用默认 LLM 实例（单例）")
            return cls._default_instance

        # 确定最终参数
        final_temp = (
            temperature if temperature is not None else settings.LLM_TEMPERATURE
        )
        final_model = model_name if model_name is not None else settings.LLM_MODEL_NAME

        # 如果不缓存，直接创建新实例
        if not use_cache:
            print(f"🆕 创建临时实例: model={final_model}, temp={final_temp}")
            return cls._create_llm(final_model, final_temp)

        # 使用缓存
        cache_key = (final_model, final_temp)
        if cache_key not in cls._custom_instances:
            print(f"🏗️ 创建并缓存实例: model={final_model}, temp={final_temp}")
            cls._custom_instances[cache_key] = cls._create_llm(final_model, final_temp)
        else:
            print(f"♻️ 使用缓存实例: model={final_model}, temp={final_temp}")

        return cls._custom_instances[cache_key]

    @classmethod
    def _create_llm(cls, model_name, temperature):
        """内部方法：创建 LLM 实例"""
        settings = get_settings()
        return ChatOpenAI(
            model=model_name,
            openai_api_base=settings.LLM_API_BASE_URL,
            openai_api_key=settings.LLM_API_KEY,
            temperature=temperature,
            # max_tokens=settings.LLM_MAX_TOKENS,
        )

    @classmethod
    def reset(cls):
        """重置所有缓存（用于测试）"""
        cls._default_instance = None
        cls._custom_instances = {}
        print("🔄 已重置所有 LLM 实例缓存")

    @classmethod
    def get_cache_info(cls):
        """获取缓存信息（调试用）"""
        info = {
            "default_instance": cls._default_instance is not None,
            "custom_instances_count": len(cls._custom_instances),
            "custom_configs": list(cls._custom_instances.keys()),
        }
        return info


# 便捷函数：直接获取 LLM
def get_llm(temperature=None, model_name=None, use_cache=True):  # 默认使用cache
    """
    便捷函数：获取 LLM 实例

    参数:
        temperature: 温度参数（0-1）
        model_name: 模型名称
        use_cache: 是否缓存实例

    使用示例:
        from app.core.llm_factory import get_llm

        # 最常用：默认配置
        llm = get_llm()

        # 自定义配置 （默认使用缓存）
        llm = get_llm(temperature=0.9)

        # 自定义配置
        llm = get_llm(model_name="deepseek-reasoner")

        # 不缓存
        llm = get_llm(temperature=0.5, use_cache=False)
    """
    return LLMFactory.get_llm(temperature, model_name, use_cache)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🧪 测试 LLM 工厂（混合模式）")
    print("=" * 70)

    # ========== 测试1：默认单例 ==========
    print("\n【测试1】默认配置（单例模式）")
    print("-" * 70)
    llm1 = get_llm()
    llm2 = get_llm()
    print(f"✅ 两次调用是同一个对象: {llm1 is llm2}")
    print(f"默认配置是0.7")

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
    print(f"✅ 这两个实例是否相同: {temp1 is temp2}")  # False 因为不缓存 每次都是新对象

    # ========== 测试4：查看缓存状态 ==========
    print("\n【测试4】缓存状态")
    print("-" * 70)
    cache_info = LLMFactory.get_cache_info()
    print(f"默认实例: {cache_info['default_instance']}")
    print(f"自定义实例数量: {cache_info['custom_instances_count']}")
    print(f"自定义配置: {cache_info['custom_configs']}")

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
