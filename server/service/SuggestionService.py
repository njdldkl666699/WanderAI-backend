from common.context import BaseContext
from model.entity import Suggestion
from server.mapper import SuggestionMapper
from model.dto import ChatMessageDTO


import uuid


async def create_suggestion(suggestion: ChatMessageDTO):
    """创建一个新的建议"""
    # uuid4生成一个唯一的建议ID
    suggestion_id = int(uuid.uuid4())
    #将新suggestion_id存储到数据库中
    account_id=BaseContext.get_account_id()
    if not account_id:
        raise ValueError("Account ID is Null")
    else:
        new_suggestion = Suggestion(id=suggestion_id, account_id=account_id, message=suggestion.message)
        await SuggestionMapper.create_suggestion(new_suggestion)

