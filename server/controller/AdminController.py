from fastapi import APIRouter, Query

from common.log import log
from model.dto import AdminLoginDTO, DeleteAccountDTO, DeleteSuggestionDTO
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


@router.get("/getAccount")
async def get_account(account_id: str = Query(None, description="用户账号", alias="accountId")):
    """查找某个用户账号和昵称"""
    user = await AdminService.get_acount(account_id)
    return Result.success(user)


@router.delete("/deleteAccount")
async def delete_account(deleteAccountDTO: DeleteAccountDTO):
    """注销账户"""
    await AdminService.delete_account(deleteAccountDTO)
    return Result.success()


@router.get("/getSuggestion")
async def get_suggestion(account_id: str = Query(None, description="用户账号", alias="accountId")):
    """查找用户建议"""
    suggestion = await AdminService.get_suggestion(account_id)
    return Result.success(suggestion)


@router.get("/getAllSuggestion")
async def get_all_suggestion():
    """查找所有用户建议"""
    suggestion = await AdminService.get_all_suggestion()
    return Result.success(suggestion)


@router.delete("/deleteSuggestion")
async def delete_suggestion(deleteSuggestionDTO: DeleteSuggestionDTO):
    """删除用户建议"""
    await AdminService.delete_suggestion(deleteSuggestionDTO)
    return Result.success()
