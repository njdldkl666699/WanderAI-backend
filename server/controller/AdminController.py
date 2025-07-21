from fastapi import APIRouter, Query

from common.log import log
from model.dto import AdminLoginDTO,DeleteAccountDTO,GetSuggestionDTO
from model.result import Result
from server.service import AdminService

router = APIRouter(prefix="/admin")


@router.post("/login")
async def login(adminLoginDTO: AdminLoginDTO):
    """管理员登录"""
    log.info(f"管理员登录: {adminLoginDTO.admin_id}")
    adminLoginVO = await AdminService.login(adminLoginDTO)
    return Result.success(adminLoginVO)

@router.get("/getUsers")
async def get_users():
    """查找所有用户账号和昵称"""
    users = await AdminService.list_users()
    return Result.success(users)

@router.delete("/deleteAccount")
async def delete_account(deleteAccountDTO:DeleteAccountDTO):
    """注销账户"""
    await AdminService.delete_account(deleteAccountDTO)
    return Result.success()

@router.get("/getSuggestion")
async def get_suggestion(getSuggestionDTO:GetSuggestionDTO):
    """查找用户建议"""
    suggestion = await AdminService.get_suggestion(getSuggestionDTO)
    return Result.success(suggestion)

    