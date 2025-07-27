from wanderai.common.constant import MessageConstant
from wanderai.common.context import BaseContext
from wanderai.common.exception import UserNotFoundException
from wanderai.model.dto import SuggestionDTO
from wanderai.model.entity import Suggestion
from wanderai.server.mapper import SuggestionMapper


async def create_suggestion(suggestion: SuggestionDTO):
    """创建一个新的建议"""
    account_id = BaseContext.get_account_id()
    if not account_id:
        raise UserNotFoundException(MessageConstant.PLEASE_LOGIN)

    # 将新suggestion_id存储到数据库中
    new_suggestion = Suggestion(id=None, account_id=account_id, message=suggestion.message)
    await SuggestionMapper.create_suggestion(new_suggestion)
