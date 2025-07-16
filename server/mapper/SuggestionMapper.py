from sqlalchemy import select, update

from common.context import BaseContext
from model.entity import Suggestion
from model.schema import SuggestionModel

async def create_suggestion(suggestion: Suggestion) -> None:
    """创建新建议"""
    db = BaseContext.get_db_session()
    suggestion_model = SuggestionModel(**suggestion.model_dump())
    db.add(suggestion_model)




