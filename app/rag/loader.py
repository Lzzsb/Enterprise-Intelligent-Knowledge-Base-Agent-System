"""
文档加载器模块
支持加载 PDF、TXT 等格式的文档

输出数据为 list[Document]
Document 对象 包含 page_content 和 metadata
"""

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader

#  PyPDFLoader, TextLoader 要求传入的文件路径是 字符串类型


class DocumentLoader:
    """文档加载器类"""

    # 支持的文件格式
    SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}

    @staticmethod  # 工具函数 没有 self、没有 cls
    def load_pdf(file_path):
        #   file_path: PDF 文件路径
        #   返回: 文档列表，每个文档包含 page_content 和 metadata

        print(f"📄 正在加载 PDF: {file_path}")
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        print(f"✅ 成功加载 {len(documents)} 页")
        return documents

    @staticmethod
    def load_txt(file_path):
        #   file_path: TXT 文件路径
        #   返回: 文档列表

        print(f"📝 正在加载 TXT: {file_path}")
        loader = TextLoader(file_path, encoding="utf-8")
        documents = loader.load()
        print(f"✅ 成功加载文本文件")
        return documents

    @staticmethod
    def load_document(file_path):
        # 自动识别文件类型并加载

        file_path = Path(
            file_path
        )  # 这里传入的可能是字符串类型所以需要转换为 Path 对象 因为后面的判断是基于path对象的

        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")

        suffix = file_path.suffix.lower()  # suffix 是文件后缀名 如 .pdf .txt .md

        if suffix == ".pdf":
            return DocumentLoader.load_pdf(str(file_path))
            # PyPDFLoader 要求传入的文件路径是 字符串类型
        elif suffix in [".txt", ".md"]:
            return DocumentLoader.load_txt(str(file_path))
            # TextLoader 要求传入的文件路径是 字符串类型
        else:
            raise ValueError(f"不支持的文件格式: {suffix}")

    @staticmethod
    def load_directory(directory_path, recursive=False):
        """
        批量加载文件夹内的所有文档

        参数:
            directory_path: 文件夹路径
            recursive: 是否递归处理子文件夹（默认False）

        返回:
            所有文档的列表

        使用示例:
            # 只处理当前文件夹
            docs = DocumentLoader.load_directory("./docs")

            # 递归处理所有子文件夹
            docs = DocumentLoader.load_directory("./docs", recursive=True)
        """
        directory_path = Path(directory_path)

        if not directory_path.exists():
            raise FileNotFoundError(f"文件夹不存在: {directory_path}")

        if not directory_path.is_dir():
            raise ValueError(f"路径不是文件夹: {directory_path}")

        print(f"\n📂 正在扫描文件夹: {directory_path}")
        print(f"   递归模式: {'是' if recursive else '否'}")

        # 查找所有支持的文件
        all_files = []
        if recursive:
            # 递归查找所有子文件夹（rglob = recursive glob）
            for ext in DocumentLoader.SUPPORTED_EXTENSIONS:
                all_files.extend(
                    directory_path.rglob(f"*{ext}")
                )  # 通配符模式 * 表示匹配任意字符 如 *.pdf 表示匹配所有 pdf 文件
        else:
            # 只查找当前文件夹（glob）
            for ext in DocumentLoader.SUPPORTED_EXTENSIONS:
                all_files.extend(directory_path.glob(f"*{ext}"))

        if not all_files:
            print(
                f"⚠️ 未找到支持的文件（支持格式: {DocumentLoader.SUPPORTED_EXTENSIONS}）"
            )
            return []

        print(f"✅ 找到 {len(all_files)} 个文件")

        # 按文件类型分组显示 计数
        file_types = {}  # 是字典的形式 如 {'.pdf': 10, '.txt': 20, '.md': 5}
        for file in all_files:
            ext = file.suffix.lower()
            file_types[ext] = file_types.get(ext, 0) + 1
            # file_types.get(ext, 0)表示获取 ext 对应的值 如果 ext 不存在则返回 0

        for ext, count in sorted(file_types.items()):
            # .items() 返回的是一个元组列表 如 [('.pdf', 10), ('.txt', 20), ('.md', 5)]
            # 在这里是按key 后缀名排序 而不是value值
            print(f"   - {ext}: {count} 个")

        # 批量加载所有文档
        all_documents = []
        success_count = 0
        failed_files = []

        print(f"\n📖 开始加载文档...")
        for i, file_path in enumerate(all_files, 1):
            try:
                print(f"\n[{i}/{len(all_files)}] 处理: {file_path.name}")
                docs = DocumentLoader.load_document(str(file_path))
                all_documents.extend(docs)
                success_count += 1
            except Exception as e:
                print(f"❌ 加载失败: {e}")
                failed_files.append((file_path.name, str(e)))

        # 显示总结
        print(f"\n📊 批量加载完成！")
        print(f"✅ 成功: {success_count}/{len(all_files)} 个文件")
        print(f"📄 总文档块数: {len(all_documents)}")

        if failed_files:
            print(f"\n⚠️ 失败的文件:")
            for filename, error in failed_files:
                print(f"   - {filename}: {error}")

        return all_documents


# 便捷函数
def load_document(file_path):
    # 加载单个文档
    return DocumentLoader.load_document(file_path)


def load_directory(directory_path, recursive=False):
    # 批量加载文件夹内的文档

    # 加载当前文件夹的所有文档
    # docs = load_directory("./docs")

    # 递归加载所有子文件夹
    # docs = load_directory("./docs", recursive=True)

    return DocumentLoader.load_directory(directory_path, recursive)


if __name__ == "__main__":
    print("=" * 70)
    print("🧪 测试文档加载器")
    print("=" * 70)

    docs = load_directory(".\docs")
    print(f"\n文档数量: {len(docs)}")
    print(f"文档内容预览:\n{docs[0].page_content[:200]}...")
    print(f"文档元数据: {docs[0].metadata}")

    # docs数据类型是 list[Document] 列表中每个元素都是 Document 对象
    # docs[0] 是一个 Document 对象 包含 page_content 和 metadata

    # print(f"输出数据预览:{docs[0]}")
