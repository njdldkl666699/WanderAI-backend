from langgraph.prebuilt import create_react_agent

from server.agent.llm import chat_llm, hotspot_llm, intent_llm, plan_llm, summary_llm
from server.agent.output_parser import intent_parser
from server.agent.prompt_template import intent_prompt_template
from server.agent.tool import calculator, search_tool

hotspot_agent_executor = create_react_agent(model=hotspot_llm, tools=[search_tool])

intent_chain = intent_prompt_template | intent_llm | intent_parser

chat_agent = create_react_agent(
    model=chat_llm,
    tools=[search_tool],
)

plan_agent = create_react_agent(
    model=plan_llm,
    tools=[search_tool],
)

summary_agent = create_react_agent(model=summary_llm, tools=[calculator])
