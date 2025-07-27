import math
from contextlib import asynccontextmanager

import numexpr
from langchain.tools import tool
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_tavily import TavilySearch
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from wanderai.common.properties import AMAP_MCP_URL

# 搜索工具
search_tool = TavilySearch(max_results=5)


@tool
def calculator(expression: str) -> str:
    """Calculate expression using Python's numexpr library.

    Expression should be a single line mathematical expression
    that solves the problem.

    Examples:
        "37593 * 67" for "37593 times 67"
        "37593**(1/5)" for "37593^(1/5)"
    """
    local_dict = {"pi": math.pi, "e": math.e}
    return str(
        numexpr.evaluate(
            expression.strip(),
            global_dict={},  # restrict access to globals
            local_dict=local_dict,  # add common mathematical functions
        )
    )


@asynccontextmanager
async def load_amap_mcp_tools():
    """高德地图MCP工具"""
    async with streamablehttp_client(AMAP_MCP_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)
            yield tools
