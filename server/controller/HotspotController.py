from fastapi import APIRouter
from server import app
from typing import Dict,Any
from llm.hotspots import prompt,agent_executor,generate_response,out_parser
import json
from model.result import Result
from langchain_core.messages import HumanMessage 


router = app.APIRouter()
@router.get("/hotspots")
async def get_hotspots():
    """获取热门景点推荐"""
    response = agent_executor.invoke({
        "messages":[HumanMessage(content=prompt)]
    })
    ai_response=response["messages"][-1].content
    hotspot_response=out_parser.parse(ai_response)
    return Result.success(hotspot_response)

    

    
        
    