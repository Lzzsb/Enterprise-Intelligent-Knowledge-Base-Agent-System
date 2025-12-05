"""
向量存储模块
使用 FAISS 实现文档的向量化存储和相似度检索

特别要注意的点： 加载向量库还必须重新创建同一个 embeddings 模型

vector_store.similarity_search 返回的是 list[Document]
vector_store.similarity_search_with_score 返回的是 list[(Document, score)]

store函数保存的是index.faiss文件 和 index.pkl文件

"""

import sys
from pathlib import Path

root_location = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_location))

from langchain_community.vectorstores import FAISS
from app.core.embedding_factory import get_embeddings
from app.core.config import get_settings


class VectorStoreManager:
    """向量存储管理器"""

    @staticmethod
    def create_vector_store(documents):
        """
        从文档创建向量存储

        参数:
            documents: 文档列表（通常是切分后的文档块）

        返回:
            FAISS 向量存储实例
        """
        print(f"\n🔮 正在创建向量存储...")
        print(f"   文档块数量: {len(documents)}")

        # 获取嵌入模型
        embeddings = (
            get_embeddings()
        )  # 使用默认参数  "BAAI/bge-m3" 和 "cuda" 目前最好用的 没必要用别的

        # 创建向量存储
        print(f"   ⏳ 正在向量化文档（可能需要一些时间）...")
        vector_store = FAISS.from_documents(documents=documents, embedding=embeddings)

        print(f"✅ 向量存储创建完成！")
        return vector_store

    @staticmethod
    def save_vector_store(vector_store, save_path=None):
        """
        保存向量存储到本地

        参数:
            vector_store: FAISS 向量存储实例
            save_path: 保存路径，None则使用配置文件路径
        """
        settings = get_settings()
        final_path = save_path if save_path is not None else settings.VECTOR_STORE_PATH

        # 创建目录
        Path(final_path).mkdir(parents=True, exist_ok=True)

        print(f"\n💾 正在保存向量存储...")
        print(f"   保存路径: {final_path}")

        vector_store.save_local(final_path)
        print(f"FAISS 保存时生成一个index.faiss文件 和一个index.pkl文件")

        print(f"✅ 向量存储已保存！")

    @staticmethod
    def load_vector_store(load_path=None):
        """
        从本地加载向量存储

        参数:
            load_path: 加载路径，None则使用配置文件路径

        返回:
            FAISS 向量存储实例
        """
        settings = get_settings()
        final_path = load_path if load_path is not None else settings.VECTOR_STORE_PATH

        if not Path(final_path).exists():
            raise FileNotFoundError(f"向量存储不存在: {final_path}")

        print(f"\n📂 正在加载向量存储...")
        print(f"   加载路径: {final_path}")

        # 创建嵌入模型（需要相同的模型来加载）
        embeddings = get_embeddings()

        # 可恶的load_local 必须创建一个模型 还必须得是和先前embeddings的相同模型 才能加载成功
        vector_store = FAISS.load_local(
            final_path,
            embeddings,
            allow_dangerous_deserialization=True,  # 允许加载.pkl文件 （无视风险）
        )

        print(f"✅ 向量存储已加载！")
        return vector_store

    @staticmethod
    def search(vector_store, query, k=3):
        """
        相似度搜索

        参数:
            vector_store: FAISS 向量存储实例
            query: 查询文本
            k: 返回最相似的前 k 个文档

        返回:
            相关文档列表
        """
        print(f"\n🔍 正在搜索: '{query}'")
        print(f"   返回文档数: {k}")

        results = vector_store.similarity_search(query, k=k)

        print(f"✅ 找到 {len(results)} 个相关文档")
        return results

    @staticmethod
    def search_with_score(vector_store, query, k=3):
        """
        带相似度分数的搜索

        参数:
            vector_store: FAISS 向量存储实例
            query: 查询文本
            k: 返回最相似的前 k 个文档

        返回:
            (文档, 相似度分数) 的列表
        """
        print(f"\n🔍 正在搜索（带分数）: '{query}'")
        print(f"   返回文档数: {k}")

        results = vector_store.similarity_search_with_score(query, k=k)

        print(f"✅ 找到 {len(results)} 个相关文档")
        return results


# 便捷函数
def create_vector_store(documents):
    """创建向量存储"""
    return VectorStoreManager.create_vector_store(documents)


def save_vector_store(vector_store, save_path=None):
    """保存向量存储"""
    return VectorStoreManager.save_vector_store(vector_store, save_path)


def load_vector_store(load_path=None):
    """加载向量存储"""
    return VectorStoreManager.load_vector_store(load_path)


def search(vector_store, query, k=3):
    """搜索相似文档"""
    return VectorStoreManager.search(vector_store, query, k)


def search_with_score(vector_store, query, k=3):
    """搜索相似文档（带分数）"""
    return VectorStoreManager.search_with_score(vector_store, query, k)


if __name__ == "__main__":
    print("测试文件在misc目录下")
