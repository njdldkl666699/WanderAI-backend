from contextlib import asynccontextmanager

from langgraph.checkpoint.mysql.asyncmy import AsyncMySaver
from langgraph.graph.state import CompiledStateGraph

from common.properties import DATABASE_URL
from server.agent.graph import workflow
from server.agent.state import TravelPlanState


@asynccontextmanager
async def create_travel_plan_graph():
    """创建旅行计划图的实例"""
    # 使用 AsyncMySaver 作为检查点存储
    async with AsyncMySaver.from_conn_string(DATABASE_URL) as memory:
        await memory.setup()
        yield workflow.compile(checkpointer=memory, name="travel_plan_graph")


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
