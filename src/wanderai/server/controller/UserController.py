from fastapi import APIRouter, Query

from wanderai.common.log import log
from wanderai.model.dto import UserLoginDTO, UserRegisterDTO
from wanderai.model.result import Result
from wanderai.server.service import UserService

router = APIRouter(prefix="/user")


@router.post("/login")
async def login(userLoginDTO: UserLoginDTO):
    """用户登录"""
    log.info(f"用户登录: {userLoginDTO.account_id}")
    userLoginVO = await UserService.login(userLoginDTO)
    return Result.success(userLoginVO)


@router.post("/register")
async def register(userRegisterDTO: UserRegisterDTO):
    """用户注册"""
    log.info(f"用户注册: {userRegisterDTO.nickname}")
    userRegisterVO = await UserService.register(userRegisterDTO)
    return Result.success(userRegisterVO)


@router.put("/nickname")
async def update_user(new_nickname: str = Query(alias="newNickname")):
    """修改昵称"""
    log.info(f"更新用户昵称: {new_nickname}")
    await UserService.update(new_nickname)
    return Result.success()
