import json
from typing import Any, Tuple
from server.agent.graph import create_travel_plan_graph
from server.agent.model import FinalOutput
from langgraph.graph.state import CompiledStateGraph

from server.agent.state import TravelPlanState
from langchain_core.runnables import RunnableConfig


async def get_or_create_state(
    app: CompiledStateGraph[TravelPlanState, TravelPlanState, TravelPlanState],
    user_input: str,
    thread_id: str,
) -> TravelPlanState:
    """获取或创建初始状态，保持历史记忆"""

    # 获取最新的检查点状态
    state_snapshot = await app.aget_state({"configurable": {"thread_id": thread_id}})

    if state_snapshot and state_snapshot.values:
        # 如果存在历史状态，更新用户输入
        existing_state = state_snapshot.values
        existing_state["user_input"] = user_input
        return TravelPlanState(**existing_state)
    else:
        # 如果不存在，创建新状态
        return {
            "user_input": user_input,
            "intent_type": "chat",
            "location": "",
            "duration": 0,
            "daily_schedules": [],
            "executor_results": [],
            "summary_result": {},
            "final_output": "",
            "messages": [],
        }


async def travel_plan_or_chat(session_id: str, message: str):
    """进行一次旅行计划或聊天交互"""
    # 创建旅行计划图
    async with create_travel_plan_graph() as app:
        # 获取初始状态
        initial_state = await get_or_create_state(app, message, thread_id=session_id)

        # 初始化当前节点
        current_node: str = ""

        # 使用astream方法进行流式处理
        # 使用混合流式处理模式
        async for chunk in app.astream(
            initial_state,
            config=RunnableConfig(configurable={"thread_id": session_id}),
            stream_mode=["updates", "messages"],
            subgraphs=True,
        ):
            (_, stream_mode, message_tuple) = chunk
            if stream_mode == "updates":
                message_dict: dict[str, Any] = message_tuple  # type: ignore
                # 这里得到了TravelPlanState的更新
                # current_state: TravelPlanState = message_dict["intent_recognition"]
                keys = message_dict.keys()
                print(f"\n\n状态更新: {keys}\n")

            if stream_mode == "messages":
                (message_chunk, metadata) = message_tuple  # type: ignore
                metadata: dict[str, Any] = metadata
                node_name = metadata["langgraph_node"]
                if current_node != node_name:
                    print(f"\n{"#"*20} 当前节点：{node_name} {"#"*20}\n")
                    current_node = node_name

                if current_node == "chat":
                    print(message_chunk.content, end="", flush=True)

        # 最终状态
        final_state = await app.aget_state({"configurable": {"thread_id": session_id}})

        if final_state and final_state.values:
            final_output_dict = final_state.values.get("final_output", "")
            print("\n\n最终输出:")
            print(json.dumps(final_output_dict, ensure_ascii=False, indent=2))
