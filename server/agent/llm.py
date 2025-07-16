from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from common.properties import (
    CHAT_LLM_NAME,
    CHAT_TEMPERATURE,
    EXECUTOR_LLM_NAME,
    EXECUTOR_TEMPERATURE,
    HOTSPOT_LLM_NAME,
    HOTSPOT_TEMPERATURE,
    INTENT_LLM_NAME,
    INTENT_TEMPERATURE,
    PLAN_LLM_NAME,
    PLAN_TEMPERATURE,
    QWEN_API_KEY,
    QWEN_BASE_URL,
    SUMMARY_LLM_NAME,
    SUMMARY_TEMPERATURE,
)

hotspot_llm = ChatOpenAI(
    model=HOTSPOT_LLM_NAME,
    api_key=SecretStr(QWEN_API_KEY),
    base_url=QWEN_BASE_URL,
    temperature=HOTSPOT_TEMPERATURE,
)

intent_llm = ChatOpenAI(
    model=INTENT_LLM_NAME,
    api_key=SecretStr(QWEN_API_KEY),
    base_url=QWEN_BASE_URL,
    temperature=INTENT_TEMPERATURE,
)

chat_llm = ChatOpenAI(
    model=CHAT_LLM_NAME,
    api_key=SecretStr(QWEN_API_KEY),
    base_url=QWEN_BASE_URL,
    temperature=CHAT_TEMPERATURE,
)

plan_llm = ChatOpenAI(
    model=PLAN_LLM_NAME,
    api_key=SecretStr(QWEN_API_KEY),
    base_url=QWEN_BASE_URL,
    temperature=PLAN_TEMPERATURE,
)

executor_llm = ChatOpenAI(
    model=EXECUTOR_LLM_NAME,
    api_key=SecretStr(QWEN_API_KEY),
    base_url=QWEN_BASE_URL,
    temperature=EXECUTOR_TEMPERATURE,
)

summary_llm = ChatOpenAI(
    model=SUMMARY_LLM_NAME,
    api_key=SecretStr(QWEN_API_KEY),
    base_url=QWEN_BASE_URL,
    temperature=SUMMARY_TEMPERATURE,
)
