import uuid
from typing import Any, AsyncGenerator

from langchain_core.messages.ai import AIMessageChunk
from langchain_core.runnables.config import RunnableConfig

from common.constant import MessageConstant
from common.context import BaseContext
from common.exception import MessageCannotBeEmptyException, UserNotFoundException
from common.log import log
from model.dto import ChatMessageDTO
from model.entity import UserHistory
from model.result import StreamResult
from model.vo import CreateSessionVO
from server.agent.interface import TravelChatAgent
from server.mapper import UserHistoryMapper


async def create_session() -> CreateSessionVO:
    """创建一个新的会话"""
    # uuid4生成一个唯一的会话ID
    session_id = str(uuid.uuid4())
    # 将新session_id存储到数据库中
    account_id = BaseContext.get_account_id()
    if not account_id:
        raise UserNotFoundException(MessageConstant.PLEASE_LOGIN)

    # 生成session_id放到数据库
    new_user_history = UserHistory(
        id=None, account_id=account_id, session_id=session_id, title="新建对话"
    )
    await UserHistoryMapper.create_user_history(new_user_history)

    # 返回创建会话的VO对象
    return CreateSessionVO(session_id=session_id)


async def travel_plan_or_chat(
    chat_message_dto: ChatMessageDTO, session_id: str
) -> AsyncGenerator[str, None]:
    """异步流式聊天生成器"""
    try:
        message = chat_message_dto.message
        # 检查消息内容是否为空
        if not message or not message.strip():
            raise MessageCannotBeEmptyException(MessageConstant.MESSAGE_CANNOT_BE_EMPTY)

        # 创建旅行计划图
        async for graph in TravelChatAgent.create_travel_plan_graph():
            # 获取初始状态
            initial_state = await TravelChatAgent.get_or_create_state(
                graph, message, thread_id=session_id
            )

            # 初始化当前节点
            current_node: str = ""

            # 使用updates和messages混合流式处理模式
            async for chunk in graph.astream(
                initial_state,
                config=RunnableConfig(configurable={"thread_id": session_id}),
                stream_mode=["updates", "messages"],
                subgraphs=True,
            ):
                (namespace, mode, data) = chunk

                parent_name = ""
                # 获取当前节点的父节点名称
                if namespace and len(namespace) != 0:
                    parent_name = namespace[0]

                if mode == "updates":
                    # 这里得到了TravelPlanState的更新
                    message_dict: dict[str, Any] = data  # type: ignore
                    key = list(message_dict.keys())[0]
                    # current_state: TravelPlanState = message_dict[key]
                    log.info(f"\n{"#"*20} 状态更新: {parent_name} {key} {"#"*20}\n")

                    # 映射节点到处理消息
                    processing_message = map_node_to_processing_message(parent_name, key)
                    plan_result = StreamResult.plan(processing_message)
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
            final_state = await graph.aget_state({"configurable": {"thread_id": session_id}})

            if final_state and final_state.values:
                final_output: dict[str, Any] | str = final_state.values.get("final_output", "")

                if isinstance(final_output, str):
                    # chat输出
                    log.info(f"最终输出：{final_output}")
                if isinstance(final_output, dict):
                    # 旅行规划输出
                    log.info(f"最终输出：{final_output.keys()}")

                all_result = StreamResult.all(final_output)
                yield all_result.to_sse_format()

        # 结束标识
        log.info("流式对话结束")
        end_result = StreamResult.end()
        yield end_result.to_sse_format()

    except Exception as e:
        log.error(f"流式对话出错: {e}")
        error_result = StreamResult.error(f"流式对话出错: {str(e)}")
        yield error_result.to_sse_format()


def map_node_to_processing_message(parent: str, node: str) -> str:
    """将节点信息映射到处理消息"""
    # 节点映射
    node_mapping = {
        "intent_recognition": "意图识别",
        "planning": "整体计划",
        "executor": "每日规划",
        "summary": "总结",
        "chat": "聊天",
    }

    # 父节点映射
    parent_node_mapping = {
        "planning": "整体计划Agent",
        "executor": "每日规划Agent",
        "summary": "总结Agent",
        "chat": "聊天Agent",
    }

    if not parent:
        return node_mapping.get(node, "")

    # 检查 parent 中是否包含映射键
    for key, value in parent_node_mapping.items():
        if key in parent:
            return value

    return ""
