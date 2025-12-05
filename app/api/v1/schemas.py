# 定义API的请求和响应的schema （格式化的数据结构）

from pydantic import BaseModel, Field

# basemodel 是所有schema的基类
# field 是用于定义字段的类


class ChatRequest(BaseModel):
    query: str = Field(
        ..., description="用户的问题", example="巴西庞大的咖啡产业起源于什么时候？"
    )
    use_search: bool = Field(
        False, description="是否强制使用联网搜索"
    )  # 是否强制使用联网搜索 默认不使用


class ChatResponse(BaseModel):
    answer: str = Field(..., description="回答")
    source_documents: list[str] = Field(None, description="参考的文档来源（如果有）")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="错误信息")


class HealthCheck(BaseModel):
    status: str = "ok"
