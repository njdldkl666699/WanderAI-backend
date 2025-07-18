from langgraph.graph import END, StateGraph

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
