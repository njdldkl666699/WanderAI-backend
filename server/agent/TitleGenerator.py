from langchain_core.messages import BaseMessage

from agent.runnable import title_chain


def generate_title(messages: list[BaseMessage]) -> str:
    """生成标题"""
    title = title_chain.invoke({"messages": messages})
    return title
