import uuid
from typing import Any

from langchain_core.messages import AIMessageChunk
from langgraph.graph.state import CompiledStateGraph

from agent.message import AIAudioMessage
from agent.state import TravelPlanState
from common.constant import MessageConstant
from common.exception import MessageListEmptyException
from common.log import log
from common.util import AliOssUtil
from model.dto import GuideMessageDTO
from model.result import StreamResult
from server.agent import TravelChatAgent, TravelGuideAgent
from server.agent.TravelGuideAgent import generate_audio_from_text, travel_guide_graph


async def travel_guide(guide_message_dto: GuideMessageDTO, session_id: str):
    """向导游发送消息"""
    image_url = guide_message_dto.image_url
    message = guide_message_dto.message
    try:
        if not image_url:
            raise MessageListEmptyException(MessageConstant.IMAGE_CANNOT_BE_EMPTY)

        # 创建旅行计划图，从中获得历史消息
        async for graph in TravelChatAgent.create_travel_plan_graph():
            travel_guide_state = await TravelGuideAgent.get_or_create_state(
                graph, message, image_url, session_id
            )
            log.info(f"导游回复消息开始，会话ID: {session_id}")

            # 发送消息到旅行导游图
            async for chunk in travel_guide_graph.astream(
                travel_guide_state,
                {"configurable": {"thread_id": session_id}},
                stream_mode="messages",
                subgraphs=True,
            ):
                (namespace, (message_chunk, metadata)) = chunk  # type: ignore
                namespace: tuple[str] = namespace
                message_chunk: AIMessageChunk = message_chunk
                metadata: dict[str, Any] = metadata
                node_name = metadata["langgraph_node"]

                parent_name = ""
                # 获取当前节点的父节点名称
                if namespace and len(namespace) != 0:
                    parent_name = namespace[0]

                if "text" in parent_name and "agent" in node_name:
                    # 如果父节点是文本节点且子节点不是工具节点，
                    # 直接输出流式文本消息
                    content: str = message_chunk.content  # type: ignore
                    print(content, end="", flush=True)
                    chat_result = StreamResult.chat(content)
                    yield chat_result.to_sse_format()

            log.info(f"导游回复消息流式输出完成，会话ID: {session_id}")

            # 创建音频输出
            audio_url = await create_audio_output(graph, session_id)
            audio_result = StreamResult.audio(audio_url)
            yield audio_result.to_sse_format()

        # 发送结束标志
        log.info(f"导游回复消息完成，会话ID: {session_id}")
        end_result = StreamResult.end()
        yield end_result.to_sse_format()

    except Exception as e:
        log.error(f"导游回复消息失败: {e}", exc_info=e, stack_info=True)
        error_result = StreamResult.error(f"流式对话失败：{str(e)}")
        yield error_result.to_sse_format()


async def create_audio_output(
    graph: CompiledStateGraph[TravelPlanState, TravelPlanState, TravelPlanState], session_id: str
):
    # 获取最终状态，获取文本结果
    final_state = await travel_guide_graph.aget_state({"configurable": {"thread_id": session_id}})
    text_result = final_state.values["text_result"]

    # 调用音频合成服务，并上传音频到OSS
    audio_data = generate_audio_from_text(text_result)
    audio_name = f"audios/{uuid.uuid4()}.wav"
    audio_url = AliOssUtil.put_object(audio_name, audio_data)

    # 将音频URL添加到旅行导游状态
    final_state.values["messages"].append(AIAudioMessage(audio_url, text_result))

    # 更新旅行计划图状态的历史消息，追加最后两条
    plan_state = await TravelChatAgent.get_or_create_state(graph, "", session_id)
    plan_state["messages"].extend(final_state.values["messages"][-2:])  # 保留最后两条消息
    await graph.aupdate_state(
        {"configurable": {"thread_id": session_id}}, plan_state, as_node="__start__"
    )

    # 返回音频URL
    return audio_url
