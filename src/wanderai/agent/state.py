from typing import Any, Dict, List, Literal, TypedDict

from langchain_core.messages import BaseMessage


class TravelPlanState(TypedDict):
    """旅行规划图的节点状态"""

    user_input: str  # 用户输入原文
    intent_type: Literal["plan", "chat"]  # 意图类型
    location: str  # 目的地
    duration: int  # 游玩时间
    daily_schedules: List[Dict[str, Any]]  # 计划Agent的执行结果
    executor_results: List[Dict[str, Any]]  # 执行Agent的结果列表
    summary_result: Dict[str, Any]  # 总结Agent的执行结果
    final_output: str | Dict[str, Any]  # 最终的输出
    messages: List[BaseMessage]  # 历史消息记录


class TravelGuideState(TypedDict):
    """旅游向导图的节点状态"""

    user_input: str | None  # 用户发送的原文
    image_url: str  # 用户发送的图片URL
    visual_result: str  # 视觉模型的结果
    text_result: str  # 文本模型的结果
    messages: List[BaseMessage]  # 历史消息记录
