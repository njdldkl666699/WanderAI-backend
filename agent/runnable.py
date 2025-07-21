from dashscope.audio.tts import SpeechSynthesizer
from langgraph.prebuilt import create_react_agent

from agent.llm import (
    chat_llm,
    hotspot_llm,
    intent_llm,
    plan_llm,
    summary_llm,
    text_llm,
    title_llm,
)
from agent.output_parser import intent_parser, title_parser
from agent.prompt_template import (
    intent_prompt_template,
    title_prompt_template,
)
from agent.tool import calculator, load_amap_mcp_tools, search_tool
from common.properties import SPEECH_MODEL

hotspot_agent_executor = create_react_agent(model=hotspot_llm, tools=[search_tool])

intent_chain = intent_prompt_template | intent_llm | intent_parser

title_chain = title_prompt_template | title_llm | title_parser

chat_agent = create_react_agent(
    model=chat_llm,
    tools=[search_tool],
)

plan_agent = create_react_agent(
    model=plan_llm,
    tools=[search_tool],
)

summary_agent = create_react_agent(model=summary_llm, tools=[calculator])

text_agent = create_react_agent(
    model=text_llm,
    tools=[search_tool, load_amap_mcp_tools],
)


def generate_audio_from_text(text: str) -> bytes:
    """从文本生成音频"""
    audio_result = SpeechSynthesizer.call(model=SPEECH_MODEL, text=text)
    return audio_result.get_audio_data()
