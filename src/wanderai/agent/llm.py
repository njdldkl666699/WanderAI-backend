from langchain_openai import ChatOpenAI

from wanderai.common.properties import (
    CHAT_CONFIG,
    EXECUTOR_CONFIG,
    HOTSPOT_CONFIG,
    INTENT_CONFIG,
    PLAN_CONFIG,
    SUMMARY_CONFIG,
    TEXT_CONFIG,
    TITLE_CONFIG,
    VISUAL_CONFIG,
)

hotspot_llm = ChatOpenAI(**HOTSPOT_CONFIG.model_dump())

title_llm = ChatOpenAI(**TITLE_CONFIG.model_dump())

intent_llm = ChatOpenAI(**INTENT_CONFIG.model_dump())

chat_llm = ChatOpenAI(**CHAT_CONFIG.model_dump())

plan_llm = ChatOpenAI(**PLAN_CONFIG.model_dump())

executor_llm = ChatOpenAI(**EXECUTOR_CONFIG.model_dump())

summary_llm = ChatOpenAI(**SUMMARY_CONFIG.model_dump())

visual_llm = ChatOpenAI(**VISUAL_CONFIG.model_dump())

text_llm = ChatOpenAI(**TEXT_CONFIG.model_dump())
