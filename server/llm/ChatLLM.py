from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from common.constant.MessageConstant import MODEL_NOT_FOUND, SESSION_NOT_FOUND
from common.exception import ModelNotFoundException, SessionNotFoundException
from common.properties import CHAT_MODELS

# 存储每个会话的消息历史
chat_message_history: dict[str, BaseChatMessageHistory] = {}
# 存储多模型的RunnableWithMessageHistory实例
chat_multi_model_with_history: dict[str, RunnableWithMessageHistory] = {}


async def init_llm():
    """初始化所有聊天模型"""
    # 遍历配置文件中的模型配置
    for model, model_entity in CHAT_MODELS.items():
        # 创建ChatOpenAI实例
        chat_model = ChatOpenAI(**model_entity.model_dump())
        # 创建一个RunnableWithMessageHistory实例
        chat_multi_model_with_history[model] = RunnableWithMessageHistory(
            chat_model, get_session_history
        )


def create_session(session_id: str):
    """创建一个新的会话"""
    chat_message_history[session_id] = ChatMessageHistory()


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """获取当前会话的历史消息"""
    if session_id not in chat_message_history:
        raise SessionNotFoundException(SESSION_NOT_FOUND)
    # 返回对应会话的消息历史
    return chat_message_history[session_id]


def get_runnable(model: str) -> RunnableWithMessageHistory:
    """获取指定模型的RunnableWithMessageHistory实例"""
    if model not in chat_multi_model_with_history:
        raise ModelNotFoundException(MODEL_NOT_FOUND)
    # 返回对应模型的RunnableWithMessageHistory实例
    return chat_multi_model_with_history[model]


def list_models() -> list[str]:
    """获取所有可用的模型名称"""
    # 返回chat_multi_model_with_history的键列表
    return list(chat_multi_model_with_history.keys())
