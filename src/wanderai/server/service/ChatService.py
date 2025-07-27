import uuid
from datetime import date, timedelta
from typing import Any, AsyncGenerator, Dict, List, Tuple

import requests
from langchain_core.messages import AIMessageChunk
from langchain_core.runnables.config import RunnableConfig
from langgraph.graph.state import CompiledStateGraph

from wanderai.agent.message import AIPlanMessage
from wanderai.agent.model import AttractionStaticMap, ExecutorResult
from wanderai.agent.state import TravelPlanState
from wanderai.common.constant import MessageConstant
from wanderai.common.context import BaseContext
from wanderai.common.exception import MessageCannotBeEmptyException, UserNotFoundException
from wanderai.common.log import log
from wanderai.common.properties import get_geocode_url, get_static_map_url, get_weather_info_url
from wanderai.common.util import AliOssUtil
from wanderai.model.dto import ChatMessageDTO
from wanderai.model.entity import UserHistory
from wanderai.model.result import StreamResult
from wanderai.model.vo import CreateSessionVO, Weather, WeatherVO
from wanderai.server.agent import TravelChatAgent
from wanderai.server.mapper import UserHistoryMapper


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

            # 使用 updates 和 messages 混合流式处理模式
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
                    log.info(f"\n{'#' * 20} 状态更新: {parent_name} {key} {'#' * 20}\n")

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
                        log.info(f"\n{'#' * 20} 当前节点：{parent_name} {node_name} {'#' * 20}\n")
                        current_node = node_name

                    if "chat" in parent_name and "agent" in node_name:
                        # 如果父节点是聊天节点且子节点不是工具节点，
                        # 直接输出流式聊天消息
                        content: str = message_chunk.content  # type: ignore
                        print(content, end="", flush=True)
                        chat_result = StreamResult.chat(content)
                        yield chat_result.to_sse_format()

            # 生成最终状态并输出
            final_output = await create_final_output(graph, session_id)
            if isinstance(final_output, dict):
                # 结果为旅行计划时输出
                all_result = StreamResult.all(final_output)
                yield all_result.to_sse_format()

        # 结束标识
        log.info("流式对话结束")
        end_result = StreamResult.end()
        yield end_result.to_sse_format()

    except Exception as e:
        log.error(f"流式对话出错: {e}", exc_info=e)
        error_result = StreamResult.error(f"流式对话出错: {str(e)}")
        yield error_result.to_sse_format()


async def create_final_output(
    graph: CompiledStateGraph[TravelPlanState, TravelPlanState, TravelPlanState], session_id: str
) -> dict[str, Any] | str:
    """创建最终输出，旅行计划或聊天消息"""
    final_state = await graph.aget_state({"configurable": {"thread_id": session_id}})

    if not final_state or not final_state.values:
        log.warning("没有找到最终状态，可能是会话已结束或不存在")
        return ""

    final_output: dict[str, Any] | str = final_state.values.get("final_output", "")

    if isinstance(final_output, str):
        # chat输出
        log.info(f"最终输出：{final_output}")

    if isinstance(final_output, dict):
        # 旅行规划输出
        (province, city) = set_attraction_maps(final_output)
        final_output["weather_vo"] = get_weather(province, city).model_dump()

        # 更新state的final_output
        final_state.values["final_output"] = final_output
        # 将消息追加到 messages 中
        # OpenAI 格式
        final_state.values["messages"].append(AIPlanMessage(final_output))
        # 更新状态节点（保存到检查点）
        await graph.aupdate_state(
            config={"configurable": {"thread_id": session_id}},
            values=final_state.values,
        )

        log.info(f"最终输出：{final_output.keys()}")

    return final_output


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


def set_attraction_maps(final_output: dict[str, Any]) -> Tuple[str, str]:
    """设置景点静态地图，返回省份和城市"""
    # 从 executor_results 中获取景点名称
    executor_results = final_output.get("executor_results", [])
    executor_result_list = [
        ExecutorResult.model_validate(executor_result) for executor_result in executor_results
    ]

    # 根据景点名称获取静态地图URL
    attraction_maps: List[Dict[str, Any]] = []

    province: str = ""
    city: str = ""

    for executor_result in executor_result_list:
        # 从每日行程的景点详细信息中提取景点名称
        for attraction_detail in executor_result.attraction_details:
            address = attraction_detail.address
            attraction_name = attraction_detail.attraction

            # 根据address调用地理编码API
            geocode_url = get_geocode_url(address)
            geocode_response = requests.get(geocode_url)
            if geocode_response.status_code != 200:
                log.warning(f"高德地图地理编码API调用失败：{geocode_response.status_code}")
                continue

            # 获取经纬度信息
            resp_json = geocode_response.json()
            if not resp_json.get("geocodes"):
                log.warning(f"地理编码API未返回有效的经纬度信息：{resp_json}")
                continue

            geocode = resp_json["geocodes"][0]
            location: str = geocode["location"]
            if not province or not city:
                # 获取省份和城市，整个循环只获取一次
                province = geocode["province"]
                city = geocode["city"]

            # 更新原有的coordinates字段
            attraction_detail.coordinates = location
            static_map_url = get_static_map_url(location)

            # 上传静态地图到阿里OSS
            map_response = requests.get(static_map_url)
            if map_response.status_code != 200:
                log.warning(f"获取静态地图失败：{map_response.status_code}")
                continue

            static_map_data: bytes = map_response.content
            uuid_key = str(uuid.uuid4())
            oss_key = f"static_maps/{uuid_key}.png"
            static_map_oss_url = AliOssUtil.put_object(oss_key, static_map_data)

            # 创建景点静态地图对象
            attraction_map = AttractionStaticMap(
                attraction=attraction_name, static_map_url=static_map_oss_url
            )

            attraction_maps.append(attraction_map.model_dump())

    # 将更新后的 executor_result_list 重新赋值到 final_output
    final_output["executor_results"] = [
        executor_result.model_dump() for executor_result in executor_result_list
    ]

    # 将景点静态地图信息添加到最终输出中
    final_output["attraction_maps"] = attraction_maps

    return (province, city)


def get_weather(province: str, city: str) -> WeatherVO:
    """获取城市的天气"""
    url = get_weather_info_url(province, city)
    response = requests.get(url)
    json: dict[str, Any] = response.json()
    if json.get("status") == 400:
        log.warning(f"获取天气信息失败：{json.get('msg')}")
        return WeatherVO(province=province, city=city, weathers=[])

    resp_weathers: list[dict[str, Any]] = json.get("data", [])

    weathers: List[Weather] = []
    current_date = date.today()
    i: int = 0
    for weather in resp_weathers:
        # 日期相同时，追加到列表中
        if weather["time"] == current_date.strftime("%Y-%m-%d"):
            weathers.append(
                Weather(
                    date=weather["time"],
                    max_degree=weather["max_degree"],
                    min_degree=weather["min_degree"],
                    day_weather=weather["day_weather"],
                )
            )
            # 增加一天
            current_date += timedelta(days=1)
            i += 1
            if i == 4:
                break

    return WeatherVO(province=province, city=city, weathers=weathers)
