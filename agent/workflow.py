from langgraph.graph import END, StateGraph

from agent.node import (
    chat_node,
    executor_node,
    intent_recognition_node,
    planning_node,
    should_plan_or_chat,
    summary_node,
    text_node,
    visual_node,
)
from agent.state import TravelGuideState, TravelPlanState


def create_travel_plan_workflow():
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


travel_plan_workflow = create_travel_plan_workflow()


def create_travel_guide_workflow():
    """创建图像识别图"""
    workflow = StateGraph(TravelGuideState)

    # 添加节点
    workflow.add_node("visual", visual_node)
    workflow.add_node("text", text_node)

    # 设置入口点
    workflow.set_entry_point("visual")

    # 添加边：visual -> text -> END
    workflow.add_edge("visual", "text")
    workflow.add_edge("text", END)

    return workflow


travel_guide_workflow = create_travel_guide_workflow()
