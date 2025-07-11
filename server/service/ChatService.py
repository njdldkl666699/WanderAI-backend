import uuid

from common.constant.MessageConstant import (
    MESSAGE_CANNOT_BE_EMPTY,
    MODEL_CANNOT_BE_EMPTY,
)
from common.exception import ModelNotFoundException
from common.log import log
from model.dto import ChatMessageDTO
from model.result import StreamResult
from model.vo import CreateSessionVO
from server.llm import ChatLLM


def create_session() -> CreateSessionVO:
    """创建一个新的会话"""
    # uuid4生成一个唯一的会话ID
    session_id = str(uuid.uuid4())
    # 调用ChatLLM的create_session方法创建会话
    ChatLLM.create_session(session_id)
    # 返回创建会话的VO对象
    return CreateSessionVO(session_id=session_id)


def list_models() -> list[str]:
    """获取可用的模型列表"""
    # 调用ChatLLM的list_models方法获取所有模型
    return ChatLLM.list_models()


async def stream_chat(chat_message_dto: ChatMessageDTO, session_id: str):
    """异步流式聊天生成器"""
    message = chat_message_dto.message
    model = chat_message_dto.model
    # 检查会话ID是否存在
    if not model:
        raise ModelNotFoundException(MODEL_CANNOT_BE_EMPTY)
    # 检查消息内容是否为空
    if not message or not message.strip():
        error_result = StreamResult.error(MESSAGE_CANNOT_BE_EMPTY)
        yield error_result.to_sse_format()
        return

    # 响应生成器
    try:
        # 获取指定模型的RunnableWithMessageHistory实例
        runnable = ChatLLM.get_runnable(model)

        # 获取流式调用
        chat_stream = runnable.astream(
            input={"input": message},
            config={"configurable": {"session_id": session_id}},
        )
        # 遍历流式响应
        async for chunk in chat_stream:
            if chunk.content:
                # 使用封装的StreamResult
                stream_result = StreamResult.chunk(chunk.content)
                yield stream_result.to_sse_format()

        # 发送结束标识
        end_result = StreamResult.end()
        yield end_result.to_sse_format()

    except Exception as e:
        log.error(f"流式对话出错: {e}")
        error_result = StreamResult.error(f"流式对话出错: {str(e)}")
        yield error_result.to_sse_format()
