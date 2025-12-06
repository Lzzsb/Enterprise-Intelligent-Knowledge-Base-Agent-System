"""
配置管理模块
使用 Pydantic Settings 统一管理环境变量（Environment Variables）和配置文件（.env）
"""

from pydantic_settings import BaseSettings
from typing import Optional
import torch


class Settings(BaseSettings):
    """应用配置类"""

    # 以下字段都是声明变量类型和默认值！！！！！！！！！！！！！！！！！！！！！ 并没有直接赋值

    # === LLM 配置 ===
    LLM_API_KEY: str
    LLM_API_BASE_URL: str = "https://api.deepseek.com"
    LLM_MODEL_NAME: str = "deepseek-chat"
    LLM_TEMPERATURE: float = 0.7
    # LLM_MAX_TOKENS: Optional[int] = None
    # 表示最大Token数，一定是整数  默认是None表示不限制

    # === 文本切分配置 ===
    CHUNK_SIZE: int = 300
    CHUNK_OVERLAP: int = 50

    # === 嵌入模型配置 ===
    EMBEDDING_MODEL_NAME: str = "BAAI/bge-m3"  # 1024维向量
    EMBEDDING_DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"

    # === 向量数据库配置 ===
    # VECTOR_STORE_TYPE: str = "faiss"
    VECTOR_STORE_PATH: str = "./vector_store_here"

    class Config:  # condig 内部类 配置了需要从配置文件读取的环境变量时 配置文件.env的位置

        # 从 .env 文件读取配置 （默认使用当前目录下的 .env 文件 因为.env文件不在当前目录所以需要使用绝对路径）
        import os
        from pathlib import Path

        base_dir = Path(__file__).parent.parent.parent
        env_file = os.path.join(base_dir, ".env")

        env_file_encoding = "utf-8"
        extra = "allow"  # 允许额外字段，即.env文件中没有的配置项也可以使用


# 创建全局配置实例（单例模式）
settings = Settings()


# 便捷函数：获取配置
def get_settings() -> Settings:
    """获取应用配置实例"""
    return settings


if __name__ == "__main__":
    # 测试配置是否正确加载 输出配置信息
    print("📝 配置信息:")
    print(f"LLM API Base: {settings.LLM_API_BASE_URL}")
    print(f"LLM Model: {settings.LLM_MODEL_NAME}")
    print(f"API Key: {settings.LLM_API_KEY[:10]}...")
    print(f"LLM Temperature: {settings.LLM_TEMPERATURE}")  # 控制回答的随机性，0-1之间
    print(f"Embedding Model: {settings.EMBEDDING_MODEL_NAME}")
    print(f"Vector Store Type: {settings.VECTOR_STORE_TYPE}")
