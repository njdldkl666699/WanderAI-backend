from fastapi import APIRouter

from common.log import log
from model.dto import SuggestionDTO
from model.result import Result
from server.service import SuggestionService

router = APIRouter(prefix="/suggestion")


@router.post("/")
async def create_suggestion(suggestionDTO: SuggestionDTO):
    """提交用户建议"""
    log.info(f"提交用户建议: {suggestionDTO.message}")
    await SuggestionService.create_suggestion(suggestionDTO)
    return Result.success()
