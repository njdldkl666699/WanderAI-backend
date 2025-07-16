from contextlib import asynccontextmanager
from langgraph.checkpoint.mysql.asyncmy import AsyncMySaver
from langgraph.graph import END, StateGraph

from common.context import BaseContext
from common.properties import DATABASE_URL
from server.agent.node import (
    chat_node,
    executor_node,
    intent_recognition_node,
    planning_node,
    should_plan_or_chat,
    summary_node,
)
from server.agent.state import TravelPlanState


def create_workflow():
    """创建旅行计划图"""

    workflow = StateGraph(TravelPlanState)

    # 添加节点
    workflow.add_node("intent_recognition", intent_recognition_node)
    workflow.add_node("chat", chat_node)
    workflow.add_node("planning", planning_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("summary", summary_node)

    # 设置入口点
    workflow.set_entry_point("intent_recognition")

    # 添加条件边
    workflow.add_conditional_edges(
        "intent_recognition", should_plan_or_chat, {"chat": "chat", "plan": "planning"}
    )

    # 添加边
    workflow.add_edge("chat", END)
    workflow.add_edge("planning", "executor")
    workflow.add_edge("executor", "summary")
    workflow.add_edge("summary", END)

    return workflow


workflow = create_workflow()


@asynccontextmanager
async def create_travel_plan_graph():
    """创建旅行计划图的实例"""
    # 使用 AsyncMySaver 作为检查点存储
    async with AsyncMySaver.from_conn_string(DATABASE_URL) as memory:
        await memory.setup()
        yield workflow.compile(checkpointer=memory, name="travel_plan_graph")
