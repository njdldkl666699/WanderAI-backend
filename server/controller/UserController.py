from fastapi import APIRouter

from common.log import log
from common.util import JwtUtil
from model.dto import UserLoginDTO,UserRegisterDTO,UserUpdateDTO
from model.entity import User
from model.result import Result
from model.vo import UserLoginVO
from server.service import UserService

router = APIRouter(prefix="/user")


@router.post("/login")
async def login(userLoginDTO: UserLoginDTO):
    log.info(f"用户登录: {userLoginDTO.account_id}")
    user: User = await UserService.login(userLoginDTO)

    # 登录成功后，生成jwt令牌
    token = JwtUtil.create_JWT({"user_account_id": user.account_id})
    userLoginVO = UserLoginVO(**dict(user), token=token)

    return Result.success(userLoginVO)


@router.post("/register")
async def register(userRegisterDTO: UserRegisterDTO):
    log.info(f"用户注册: {userRegisterDTO.nickname}")
    user: User = await UserService.register(userRegisterDTO)

    # 注册成功后，生成jwt令牌
    token = JwtUtil.create_JWT({"user_account_id": user.account_id})
    userLoginVO = UserLoginVO(**dict(user), token=token)

    return Result.success(userLoginVO)

"""修改昵称"""
@router.put("/nickname")
async def update_user(userUpdateDTO: UserUpdateDTO):
    log.info(f"更新用户昵称: {userUpdateDTO.newNickname}")
    user: User = await UserService.update(userUpdateDTO)
    return Result.success(user)
