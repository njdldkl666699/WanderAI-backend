from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from fastapi import APIRouter
from langchain_core.output_parsers import JsonOutputParser
from typing import Any, List
from langchain_tavily import TavilySearch
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

LOCAL_LLM_API_KEY="sk-05ce193d313e4d87bf07c8e3cf94cb1b"
LOCAL_LLM_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"

prompt = """
你是一位专业的旅游景点推荐专家。你可以调用搜索工具，得到全国的热门景点名称、描述和图片，并严格按照给定的JSON格式输出。

## 输入数据
  - 用户的需求：{input}

## 输出格式

{{
    "data": ["Hotspot"]  // 景点列表
}}

"Hotspot"定义如下：
{{
    "name": "string",  // 景点名字
    "description": "string",  // 景点描述
    "image": "string"  // 景点图片URL
}}

## 输出样例
{{
    "data": [
        {{
            "name": "天津之眼",
            "description": "天津之眼是天津的地标性建筑，拥有世界上最大的摩天轮。",
            "image": "https://example.com/tianjin_eye.jpg"
        }},
    ]
}}

请按照上述格式进行查询，完成用户的需求，不要输出其他内容，只输出JSON结果。
"""

class Hotspot(BaseModel):
    name: str
    description: str
    image: str

class HotspotsResult(BaseModel):
    data: List[Hotspot]

out_parser = JsonOutputParser(pydantic_object=HotspotsResult)

llm = ChatOpenAI(
    model="qwen-turbo",  # 确认使用DashScope支持的模型
    api_key=SecretStr(LOCAL_LLM_API_KEY),
    base_url=LOCAL_LLM_BASE_URL,
    temperature=0.2,
    )

tools = [TavilySearch()]

from langgraph.prebuilt import create_react_agent
agent_executor = create_react_agent(
    model=llm,
    tools=tools,
)

router = APIRouter()

async def generate_response() -> Any:
    """生成热门景点推荐的响应"""
    response = agent_executor.invoke({
        "messages":[("user", prompt)]
    })
    return response

#  测试
# if __name__=="__main__":
#     response = agent_executor.invoke({
#         "messages":[HumanMessage(content=prompt)]
#     })
#     ai_response=response["messages"][-1].content
#     hotspot_response=out_parser.parse(ai_response)
#     print(json.dumps(hotspot_response,ensure_ascii=False,indent=2))
        
    