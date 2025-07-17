import json
from typing import Any
import uuid

from common.constant.MessageConstant import (
    MESSAGE_CANNOT_BE_EMPTY,
    MODEL_CANNOT_BE_EMPTY,
    SESSION_NOT_FOUND,
)
from common.exception import (
    MessageCannotBeEmptyException,
    ModelNotFoundException,
    SessionNotFoundException,
)
from common.log import log
from model.dto import ChatMessageDTO
from model.result import StreamResult
from model.vo import CreateSessionVO
from server.agent.interface import TravelChatAgent
from langchain_core.runnables.config import RunnableConfig
from langchain_core.messages.ai import AIMessageChunk

from server.agent.state import TravelPlanState


def create_session() -> CreateSessionVO:
    """创建一个新的会话"""
    # uuid4生成一个唯一的会话ID
    session_id = str(uuid.uuid4())
    # 返回创建会话的VO对象
    return CreateSessionVO(session_id=session_id)


async def travel_plan_or_chat(chat_message_dto: ChatMessageDTO, session_id: str):
    """异步流式聊天生成器"""
    try:
        message = chat_message_dto.message
        # user_sessions: list[str] = UserHistoryMapper.get_session_id_by_account_id(session_id)
        # # 检查会话ID是否存在
        # if session_id not in user_sessions:
        #     raise SessionNotFoundException(SESSION_NOT_FOUND)
        # 检查消息内容是否为空
        if not message or not message.strip():
            raise MessageCannotBeEmptyException(MESSAGE_CANNOT_BE_EMPTY)

        # 创建旅行计划图
        async with TravelChatAgent.create_travel_plan_graph() as app:
            # 获取初始状态
            initial_state = await TravelChatAgent.get_or_create_state(
                app, message, thread_id=session_id
            )

            # 初始化当前节点
            current_node: str = ""

            # 使用updates和messages混合流式处理模式
            async for chunk in app.astream(
                initial_state,
                config=RunnableConfig(configurable={"thread_id": session_id}),
                stream_mode=["updates", "messages"],
                subgraphs=True,
            ):
                (namespace, mode, data) = chunk
                # parent_name: str = namespace[0]
                parent_name = ""
                if namespace and len(namespace) != 0:
                    parent_name = namespace[0]
                if mode == "updates":
                    # 这里得到了TravelPlanState的更新
                    message_dict: dict[str, Any] = data  # type: ignore
                    key = list(message_dict.keys())[0]
                    # current_state: TravelPlanState = message_dict[key]
                    log.info(f"\n{"#"*20} 状态更新: {namespace} {key} {"#"*20}\n")

                    plan_result = StreamResult.plan({"node": key, "parent": parent_name})
                    yield plan_result.to_sse_format()

                if mode == "messages":
                    (message_chunk, metadata) = data  # type: ignore
                    message_chunk: AIMessageChunk = message_chunk
                    metadata: dict[str, Any] = metadata
                    node_name = metadata["langgraph_node"]
                    if current_node != node_name:
                        log.info(f"\n{"#"*20} 当前节点：{namespace} {node_name} {"#"*20}\n")
                        current_node = node_name

                    if "chat" in parent_name:
                        # 如果父节点是聊天节点，直接输出流式聊天消息
                        content: str = message_chunk.content  # type: ignore
                        chat_result = StreamResult.chat(content)
                        yield chat_result.to_sse_format()

            # 最终状态
            final_state = await app.aget_state({"configurable": {"thread_id": session_id}})

            if final_state and final_state.values:
                final_output_dict: dict[str, Any] = final_state.values.get("final_output", "")
                log.info(f"最终输出：{final_output_dict.keys()}")
                all_result = StreamResult.all(final_output_dict)
                yield all_result.to_sse_format()

        # 结束标识
        log.info("流式对话结束")
        end_result = StreamResult.end()
        yield end_result.to_sse_format()

    except Exception as e:
        log.error(f"流式对话出错: {e}")
        error_result = StreamResult.error(f"流式对话出错: {str(e)}")
        yield error_result.to_sse_format()
