from langchain_core.messages import HumanMessage

from server.agent.model import HotspotsResult
from server.agent.output_parser import hotspot_parser
from server.agent.prompt_template import hotspot_prompt_template
from server.agent.runnable import hotspot_agent_executor


async def get_hotspots() -> HotspotsResult:
    """获取热门景点"""
    # 格式化提示词模板
    hotspot_prompt = hotspot_prompt_template.format(input="请随机推荐中国的若干个热门景点。")

    # 调用Agent
    response = await hotspot_agent_executor.ainvoke(
        {"messages": [HumanMessage(content=hotspot_prompt)]}
    )

    # 解析结果
    ai_response = response["messages"][-1].content
    hotspot_response = hotspot_parser.parse(ai_response)

    # 处理为模型类
    hotspots_result = HotspotsResult(**hotspot_response)
    return hotspots_result
