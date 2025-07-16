import json
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
    app = await create_travel_plan_graph()
    # 获取初始状态
    initial_state = await get_or_create_state(app, message, thread_id=session_id)

    # 初始化当前节点
    current_node: str = ""

    # 使用混合流式处理模式
    async for chunk in app.astream(
        initial_state,
        config=RunnableConfig(configurable={"thread_id": session_id}),
        stream_mode=["updates", "messages"],
        subgraphs=True,
    ):
        # 检查是否是消息流（用于 chat 节点的 token 流式输出）
        if hasattr(chunk, "content"):
            # 这是来自 chat 节点的流式消息
            print(chunk.content, end="", flush=True)
            continue

        # 处理节点状态更新
        for node_name, node_output in chunk.items():
            # chat 节点特殊处理 - 流式输出 token
            if node_name == "chat" or "chat" in node_name:
                # 对于 chat 节点，处理流式消息
                if isinstance(node_output, dict) and "messages" in node_output:
                    for message in node_output["messages"]:
                        if hasattr(message, "content") and message.content:
                            print(message.content, end="", flush=True)
                elif hasattr(node_output, "content") and node_output.content:
                    print(node_output.content, end="", flush=True)
            else:
                # 其他节点 - 状态更新时输出
                if current_node != node_name:
                    current_node = node_name
                    print(f"\n{'='*20} 已完成节点: {current_node} {'='*20}\n")

                    # 输出节点完成后的状态信息
                    if isinstance(node_output, dict):
                        # 可以选择性输出一些关键信息
                        if "intent_type" in node_output:
                            print(f"意图类型: {node_output['intent_type']}")
                        if "location" in node_output and node_output["location"]:
                            print(f"目的地: {node_output['location']}")
                        if "duration" in node_output and node_output["duration"]:
                            print(f"行程天数: {node_output['duration']}")
                    print()  # 换行

    # 最终状态
    final_state = await app.aget_state({"configurable": {"thread_id": session_id}})

    if final_state and final_state.values:
        final_output_dict = final_state.values.get("final_output", "")
        print("\n\n最终输出:")
        print(json.dumps(final_output_dict, ensure_ascii=False, indent=2))
