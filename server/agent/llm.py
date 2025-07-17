from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from common.properties import *

hotspot_llm = ChatOpenAI(
    model=HOTSPOT_LLM_NAME,
    api_key=SecretStr(QWEN_API_KEY),
    base_url=QWEN_BASE_URL,
    temperature=HOTSPOT_TEMPERATURE,
)

title_llm = ChatOpenAI(
    model=TITLE_LLM_NAME,
    api_key=SecretStr(QWEN_API_KEY),
    base_url=QWEN_BASE_URL,
    temperature=TITLE_TEMPERATURE,
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
