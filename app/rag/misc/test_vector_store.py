"""
测试向量存储功能
演示完整的 RAG 流程：文档加载 → 切分 → 向量化 → 检索
"""

import sys
from pathlib import Path

root_location = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root_location))


from app.rag.loader import load_document, load_directory
from app.rag.splitter import split_documents
from app.rag.vector_store import (
    create_vector_store,
    save_vector_store,
    load_vector_store,
    search,
    search_with_score,
)

print("=" * 70)
print("🧪 测试向量存储（完整 RAG 流程）")
print("=" * 70)


# 从目录加载文档
docs = load_directory(".\docs")

print(f"\n原始文档数量: {len(docs)}")
print(f"原始文档内容预览:\n{docs[0].page_content[:50]}...")
print(f"原始文档元数据: {docs[0].metadata}")

# 切分文档
chunks = split_documents(
    docs, chunk_size=250, chunk_overlap=50
)  # 默认chunk_size=300, chunk_overlap=50
print(f"切分后文档块数: {len(chunks)}")

# 预览文档块
print(f"\n切分后文档块预览(3个文档块):")
for i, chunk in enumerate(chunks[:3], 1):
    print(f"\n  块{i} (长度={len(chunk.page_content)}):")
    print(f"  {chunk.page_content[:80]}...")
    print(f"\n  块 {i} 元数据: {chunk.metadata}")

# 创建向量存储
print("\n创建向量存储...")

vector_store = create_vector_store(chunks)

# 测试相似度搜索
print("\n测试相似度搜索...")

test_queries = ["什么是深度学习？", "Python有哪些特点？", "数据科学常用工具"]

for query in test_queries:
    print(f"\n{'='*70}")
    print(f"查询: {query}")
    print("=" * 70)

    # 搜索（带分数）
    results = search_with_score(vector_store, query, k=2)

    for i, (doc, score) in enumerate(results, 1):
        print(f"\n结果{i} (相似度分数: {score:.4f}):")
        print(f"  内容: {doc.page_content[:50]}...")
        print(f"  元数据: {doc.metadata}")

# 测试保存和加载向量存储
print("\n测试保存和加载向量存储...")

save_path = "./vector_store_here"
save_vector_store(vector_store, save_path)

# 重新加载
vector_store_loaded = load_vector_store(save_path)

# 验证加载后的向量存储可用
print(f"\n验证加载的向量存储:")
test_results = search(vector_store_loaded, "机器学习", k=1)
print(f"  找到 {len(test_results)} 个相关文档")
print(f"  内容: {test_results[0].page_content[:100]}...")

# # 清理
# print("\n清理保存的向量存储...")
# shutil.rmtree(save_path) # 删除文件夹（directory）及其内部所有内容
# print("✅ 清理完成")
# print("\n" + "=" * 70)
# print("✅ 向量存储测试完成！")
# print("=" * 70)
