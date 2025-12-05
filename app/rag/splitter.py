"""
文本切分器模块
将长文档切分成适合向量化的小块

# chunks的数据类型是 list[Document] 列表中每个元素都是 Document 对象
# Document 对象 包含 page_content 和 metadata

"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


from langchain_text_splitters import RecursiveCharacterTextSplitter

# recursivecharactertextsplitter 能按多个层级（句子 -> 段落 -> 行 -> 字符）递归切割

from app.core.config import get_settings


class TextSplitter:
    """文本切分器类"""

    @staticmethod
    def create_splitter(chunk_size=None, chunk_overlap=None):
        """
        创建文本切分器

        参数:
            chunk_size: 每块的大小（字符数），None则使用配置文件
            chunk_overlap: 块之间的重叠大小，None则使用配置文件

        返回:
            文本切分器实例
        """
        settings = get_settings()

        final_chunk_size = chunk_size or settings.CHUNK_SIZE
        # 这里可以用or 因为or会把 0 False None 空值等都视为无效值 所以可以直接用or
        final_chunk_overlap = (
            chunk_overlap if chunk_overlap is not None else settings.CHUNK_OVERLAP
        )
        # 这里最好用if 因为if只会检查是不是None 只要不是None 但是为0 0可以被视为有效值 而在这里chunk_overlap可以是0

        print(f"\n🔪 创建文本切分器:")
        print(f"   - 块大小: {final_chunk_size} 字符")
        print(f"   - 重叠大小: {final_chunk_overlap} 字符")

        return RecursiveCharacterTextSplitter(
            chunk_size=final_chunk_size,
            chunk_overlap=final_chunk_overlap,
            length_function=len,  # 指定计算字符长度的函数 这里用len 因为len返回的是字符串的长度
            is_separator_regex=False,  # 指定是否使用正则表达式分割 这里用False 因为正则表达式分割可能会导致分割不准确
        )

    @staticmethod
    def split_documents(documents, chunk_size=None, chunk_overlap=None):
        """
        切分文档

        参数:
            documents: 文档列表
            chunk_size: 块大小
            chunk_overlap: 重叠大小

        返回:
            切分后的文档块列表
        """
        splitter = TextSplitter.create_splitter(chunk_size, chunk_overlap)

        print(f"\n📄 正在切分 {len(documents)} 个文档...")
        chunks = splitter.split_documents(documents)
        print(f"✅ 切分完成，共 {len(chunks)} 个文档块")

        return chunks


# 便捷函数
def split_documents(documents, chunk_size=None, chunk_overlap=None):
    """
    便捷函数：切分文档

    使用示例:
        from app.rag.splitter import split_documents
        chunks = split_documents(docs)
    """
    return TextSplitter.split_documents(documents, chunk_size, chunk_overlap)


if __name__ == "__main__":

    from loader import load_directory

    print("=" * 70)
    print("🧪 测试文本切分器")
    print("=" * 70)

    docs = load_directory(".\docs")
    chunks = split_documents(docs)

    print(f"切分后的文档块数量: {len(chunks)}")
    print(f"文档块内容预览:\n{chunks[0].page_content[:200]}...")
    print(f"文档块元数据: {chunks[0].metadata}")

    # print(type(chunks))  是list[Document] 列表中每个元素都是 Document 对象
    # print(type(chunks[0])) 是Document 对象 包含 page_content 和 metadata
