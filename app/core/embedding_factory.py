"""
嵌入模型工厂 提供文字→向量的转换能力
提供统一的嵌入模型初始化接口
嵌入embedding 是将文本转换为向量 用于计算文本相似度

直接用默认配置就行  "BAAI/bge-m3" 和 "cuda" 目前最好用的 没必要用别的

可直接通过get_embeddings(model_name=None) 获取嵌入模型实例
模型实例的 embed_query 和 embed_documents 方法可以用于将单个文本 和 多个文本转换为向量
"""

from langchain_community.embeddings import HuggingFaceEmbeddings
from .config import get_settings


class EmbeddingFactory:
    """嵌入模型工厂类（单例模式）"""

    # 默认嵌入模型实例
    _embedding_instance = None
    _cached_model_name = None

    @classmethod
    def get_embeddings(cls, model_name=None):
        """
        获取嵌入模型实例（单例模式）

        参数:
            model_name: 模型名称，None则使用配置文件

        返回:
            HuggingFaceEmbeddings 实例
        """
        # 如果已初始化，直接返回
        if cls._embedding_instance is not None:
            print("♻️ 使用已缓存的嵌入模型")
            print(f"   ⚠️ 单例模式：已忽略本次请求的模型参数")
            print(f"   - 请求的模型: {model_name}")
            print(f"   - 实际使用模型: {cls._cached_model_name}")  # 需要添加这个变量
            return cls._embedding_instance

        settings = get_settings()
        final_model = (
            model_name
            if model_name is not None
            else settings.EMBEDDING_MODEL_NAME  # 未指定模型 就用默认的 "BAAI/bge-m3"
        )

        print(f"🔧 正在初始化嵌入模型...")
        print(f"   - 模型: {final_model}")
        print(f"   - 设备: {settings.EMBEDDING_DEVICE}")
        print(f"   ⏳ 首次加载需要下载模型，请稍候...")

        # 创建嵌入模型
        cls._embedding_instance = HuggingFaceEmbeddings(
            model_name=final_model,  # 默认为"BAAI/bge-m3"
            model_kwargs={"device": settings.EMBEDDING_DEVICE},  # 设备默认为cuda
            encode_kwargs={"normalize_embeddings": True},  # 归一化向量
            # 归一化向量 是为了让向量更具有可比性 避免因为向量长度不同导致相似度计算不准确
            # 归一化向量 是将向量除以向量的模长 使得向量模长为1
            # 可以直接用点积计算相似度
        )
        # 缓存模型名称
        cls._cached_model_name = final_model

        print("✅ 嵌入模型初始化完成!")
        return cls._embedding_instance

    @classmethod
    def reset(cls):
        """重置单例（测试用）"""
        cls._embedding_instance = None


# 便捷函数
def get_embeddings(model_name=None):
    """
    便捷函数：获取嵌入模型

    使用示例:
        from app.core.embedding_factory import get_embeddings
        embeddings = get_embeddings()
    """
    return EmbeddingFactory.get_embeddings(model_name)


if __name__ == "__main__":
    print("=" * 70)
    print("🧪 测试嵌入模型工厂")
    print("=" * 70)

    embeddings = get_embeddings()
    print("\n嵌入模型初始化完成")

    print("\n 测试：嵌入单个文本")
    text = "人工智能正在改变世界"
    vector = embeddings.embed_query(text)
    # embed_query 是嵌入单个文本 返回一个向量
    print(f"文本: {text}")
    print(f"向量维度: {len(vector)}")
    print(f"向量前10个值: {vector[:10]}")

    # 测试：批量嵌入
    print("\n测试：批量嵌入多个文本")
    texts = ["机器学习是人工智能的一个分支", "深度学习使用神经网络", "今天天气真好"]
    vectors = embeddings.embed_documents(texts)
    # embed_documents 是批量嵌入多个文本 返回一个列表 列表中每个元素都是向量
    print(f"嵌入 {len(texts)} 个文本")
    print(f"每个向量维度: {len(vectors[0])}")

    # 测试：计算相似度
    print("\n测试：计算文本相似度")
    import numpy as np

    v1 = np.array(embeddings.embed_query(texts[0]))
    # v1 = np.array(vectors[0])
    v2 = np.array(embeddings.embed_query(texts[1]))
    v3 = np.array(embeddings.embed_query(texts[2]))

    # 余弦相似度（向量已归一化，直接点积即可）
    sim_12 = np.dot(v1, v2)
    sim_13 = np.dot(v1, v3)

    print(f"'{texts[0]}' vs '{texts[1]}'")
    print(f"  相似度: {sim_12:.4f}")
    print(f"\n'{texts[0]}' vs '{texts[2]}'")
    print(f"  相似度: {sim_13:.4f}")

    print("\n💡 观察：")
    print("   - AI相关的两个句子相似度更高")
    print("   - 无关的句子相似度较低")

    print("\n" + "=" * 70)
    print("✅ 嵌入模型测试完成！")
    print("=" * 70)
