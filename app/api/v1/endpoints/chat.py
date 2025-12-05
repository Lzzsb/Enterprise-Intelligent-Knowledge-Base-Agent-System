from fastapi import APIRouter, HTTPException

# APIRouter 是 FastAPI 的类，用于创建路由器 （路由器是用于将请求映射到相应的处理函数）
# HTTPException 是 FastAPI 的类，用于创建HTTP异常 返回错误给用户
from app.api.v1.schemas import ChatRequest, ChatResponse
from app.agent.executor import run_agent
import logging  # 用于记录日志

# 创建一个router 可以往router中添加多个路由接口 比如/chat /health 等
router = APIRouter()
logger = logging.getLogger(__name__)  # 日志记录器
# 使用方法： logger.error("异常发生啦！")  logger.info("信息发生啦！")  logger.warning("警告发生啦！")  logger.debug("调试发生啦！")  logger.critical("严重发生啦！")


# 表明接下来的函数是用来处理针对/chat 的post请求的 返回的数据类型必须是ChatResponse
@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    核心对话接口：
    1. 接收用户 Query
    2. 调用后端 Agent 执行
    3. 返回结果
    """
    try:
        # 获取用户输入
        user_query = request.query
        # 在这里忽视了use_search参数，因为run_agent函数没有这个参数

        # 调用 run_agent 得到agent输出
        agent_output = run_agent(user_query)

        # 构造返回结果
        return ChatResponse(
            answer=agent_output,
            source_documents=[],  # 暂时留空，后续可以从 Agent 结果里解析出来
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error内部服务器错误: {str(e)}"
        )
