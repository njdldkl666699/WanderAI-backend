from typing import Any, Dict, List

from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from langgraph.prebuilt import create_react_agent

from wanderai.agent.llm import executor_llm, visual_llm
from wanderai.agent.message import HumanImageMessage
from wanderai.agent.model import (
    ExecutorResult,
    FinalOutput,
    IntentResult,
    PlanResult,
    Schedule,
    SummaryResult,
)
from wanderai.agent.output_parser import executor_parser, plan_parser, summary_parser
from wanderai.agent.prompt_template import (
    executor_prompt_template,
    planning_prompt_template,
    summary_prompt_template,
    text_prompt_template,
    visual_prompt_template,
)
from wanderai.agent.runnable import chat_agent, intent_chain, plan_agent, summary_agent, text_agent
from wanderai.agent.state import TravelGuideState, TravelPlanState
from wanderai.agent.tool import load_amap_mcp_tools, search_tool
from wanderai.common.log import log
from wanderai.common.properties import (
    EXECUTOR_AGENT_MAX_ITERATIONS,
    PLAN_AGENT_MAX_ITERATIONS,
    SUMMARY_AGENT_MAX_ITERATIONS,
    TEXT_AGENT_MAX_ITERATIONS,
)

######################## 旅游规划图节点


def intent_recognition_node(state: TravelPlanState) -> TravelPlanState:
    """意图识别节点"""
    try:
        state["messages"].append(HumanMessage(state["user_input"]))
        response = intent_chain.invoke({"user_input": state["user_input"]})
        intent_result = IntentResult(**response)
        state["intent_type"] = intent_result.type
        if intent_result.type == "plan":
            state["location"] = intent_result.location
            state["duration"] = intent_result.duration
    except Exception as e:
        log.warning("意图识别错误：%s", e, exc_info=e)
        state["intent_type"] = "chat"
    return state


def chat_node(state: TravelPlanState) -> TravelPlanState:
    """普通聊天Agent节点"""

    messages: list[BaseMessage] = []
    for message in state["messages"]:
        if isinstance(message, AIMessage) and isinstance(message.content, list):
            message_list = message.content
            if len(message_list) == 2:
                # 去除音频URL
                text_content = ""
                for item in message_list:  # type: ignore
                    item: dict[str, str] = item
                    if item["type"] == "text":
                        text_content = item["text"]
                # 追加文本消息
                messages.append(AIMessage(text_content))
        else:
            messages.append(message)

    response = chat_agent.invoke({"messages": messages})
    ai_response = response["messages"][-1].content
    # 存入final_output
    state["final_output"] = ai_response

    ai_message = AIMessage(ai_response)
    # 更新历史记录
    messages.append(ai_message)
    return state


def planning_node(state: TravelPlanState) -> TravelPlanState:
    """计划Agent节点"""

    try:
        # 格式化提示词
        prompt_text = planning_prompt_template.format(
            location=state["location"], duration=state["duration"]
        )

        # 使用Agent
        response = plan_agent.invoke(
            {"messages": [HumanMessage(content=prompt_text)]},
            {"recursion_limit": PLAN_AGENT_MAX_ITERATIONS},
        )
        # 提取并解析结果
        ai_response = response["messages"][-1].content
        plan_response = plan_parser.parse(ai_response)
        plan_result = PlanResult(**plan_response)
        # 将结果转换为状态
        state["daily_schedules"] = [
            {"day": schedule.day, "attractions": schedule.attractions}
            for schedule in plan_result.daily_schedules
        ]
    except Exception as e:
        log.warning("计划Agent发生错误: %s", e, exc_info=e, stack_info=True)
        state["daily_schedules"] = [
            {"day": i + 1, "attractions": [f"{state['location']}景点{i + 1}"]}
            for i in range(state["duration"])
        ]

    return state


async def executor_node(state: TravelPlanState) -> TravelPlanState:
    """执行Agent节点"""

    try:
        executor_results: List[Dict[str, Any]] = []
        async with load_amap_mcp_tools() as amap_mcp_tools:
            executor_agent = create_react_agent(
                model=executor_llm, tools=[search_tool, *amap_mcp_tools]
            )

            for schedule in state["daily_schedules"]:
                print("处理第{}天的行程: {}".format(schedule["day"], schedule["attractions"]))
                day = schedule["day"]
                attractions = schedule["attractions"]

                prompt_text = executor_prompt_template.format(
                    day=day, location=state["location"], attractions=attractions
                )

                response = await executor_agent.ainvoke(
                    {"messages": [HumanMessage(content=prompt_text)]},
                    {"recursion_limit": EXECUTOR_AGENT_MAX_ITERATIONS},
                )
                # 解析结果
                ai_response = response["messages"][-1].content
                executor_response = executor_parser.parse(ai_response)
                executor_result = ExecutorResult(**executor_response)

                executor_results.append(executor_result.model_dump())

            state["executor_results"] = executor_results
    except Exception as e:
        # 生成默认执行结果
        log.warning("执行Agent发生错误: ", e, exc_info=e, stack_info=True)
        state["executor_results"] = [
            {"day": i + 1, "routes": [], "attraction_details": [], "remark_cards": {}}
            for i in range(len(state["daily_schedules"]))
        ]
    return state


def summary_node(state: TravelPlanState) -> TravelPlanState:
    """总结Agent节点"""

    try:
        # 构建每日路线列表，用于传递给总结Agent
        daily_routes_list = []
        for executor_result in state["executor_results"]:
            daily_route = {
                "day": executor_result["day"],
                "routes": executor_result["routes"],
            }
            daily_routes_list.append(daily_route)

        # 格式化提示词
        prompt_text = summary_prompt_template.format(
            user_input=state["user_input"], daily_routes_list=daily_routes_list
        )

        # 使用Agent
        result = summary_agent.invoke(
            {"messages": [HumanMessage(content=prompt_text)]},
            {"recursion_limit": SUMMARY_AGENT_MAX_ITERATIONS},
        )
        ai_response = result["messages"][-1].content
        summary_response = summary_parser.parse(ai_response)
        summary_result = SummaryResult(**summary_response)

        # 将结果转换为状态格式
        state["summary_result"] = summary_result.model_dump()

        # 生成最终输出
        final_output = generate_final_output(state)
        state["final_output"] = final_output.model_dump()

        # 更新状态，将消息追加到 messages 中
        # 在Service层处理
    except Exception as e:
        # 生成默认总结
        log.warning("总结Agent发生错误: ", e, exc_info=e, stack_info=True)
        state["summary_result"] = {
            "title": f"{state.get('location', '旅行')}计划",
            "overview": {
                "duration": f"{state.get('duration', 1)}天",
                "attraction_count": len(state.get("daily_schedules", [])),
                "total_distance": "未知",
            },
        }
        print(f"总结生成错误: {e}")

    return state


def generate_final_output(state: TravelPlanState) -> FinalOutput:
    """生成最终的旅行计划输出"""

    summary_result = SummaryResult.model_validate(state["summary_result"])
    daily_schedules = [Schedule.model_validate(schedule) for schedule in state["daily_schedules"]]
    executor_results = [
        ExecutorResult.model_validate(executor_result)
        for executor_result in state["executor_results"]
    ]

    final_output = FinalOutput(
        summary_result=summary_result,
        daily_schedules=daily_schedules,
        executor_results=executor_results,
        attraction_maps=[],  # 在Service层获取景点静态地图
        weather_vo=None,  # 在Service层获取天气信息
    )
    return final_output


# 条件函数
def should_plan_or_chat(state: TravelPlanState) -> str:
    """根据意图类型决定下一步"""
    return state["intent_type"]


###################### 旅游向导图节点


def visual_node(state: TravelGuideState) -> TravelGuideState:
    """视觉模型节点"""

    visual_prompt = visual_prompt_template.format(messages=state["messages"])

    response = visual_llm.invoke([HumanImageMessage(state["image_url"], visual_prompt)])
    if isinstance(response.content, str):
        state["visual_result"] = response.content

    return state


def text_node(state: TravelGuideState) -> TravelGuideState:
    """文本模型节点"""
    # 格式化提示词
    text_prompt = text_prompt_template.format(
        user_input=state["user_input"],
        visual_result=state["visual_result"],
        messages=state["messages"],
    )

    response = text_agent.invoke(
        {"messages": [HumanMessage(content=text_prompt)]},
        {"recursion_limit": TEXT_AGENT_MAX_ITERATIONS},
    )
    ai_result = response["messages"][-1].content
    state["text_result"] = ai_result

    # 历史消息追加用户输入和图片URL
    state["messages"].append(HumanImageMessage(state["image_url"], state["user_input"]))

    # 追加文本AI返回的消息
    # 在Service层处理

    return state
