from langchain_core.messages import BaseMessage
from langgraph.checkpoint.mysql.asyncmy import AsyncMySaver
from langgraph.graph.state import CompiledStateGraph

from wanderai.agent.state import TravelPlanState
from wanderai.agent.workflow import travel_plan_workflow
from wanderai.common.properties import DATABASE_URL


async def create_travel_plan_graph():
    """创建旅行计划图的实例"""
    # 使用 AsyncMySaver 作为检查点存储
    async with AsyncMySaver.from_conn_string(DATABASE_URL) as memory:
        await memory.setup()
        yield travel_plan_workflow.compile(checkpointer=memory, name="travel_plan_graph")


async def get_or_create_state(
    graph: CompiledStateGraph[TravelPlanState, TravelPlanState, TravelPlanState],
    user_input: str,
    thread_id: str,
) -> TravelPlanState:
    """获取或创建初始状态，保持历史记忆"""

    # 获取最新的检查点状态
    state_snapshot = await graph.aget_state({"configurable": {"thread_id": thread_id}})

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


async def get_history_messages(
    graph: CompiledStateGraph[TravelPlanState, TravelPlanState, TravelPlanState], thread_id: str
) -> list[BaseMessage]:
    """获取历史消息记录"""
    state_snapshot = await graph.aget_state({"configurable": {"thread_id": thread_id}})
    if state_snapshot and state_snapshot.values:
        return state_snapshot.values.get("messages", [])

    return []
