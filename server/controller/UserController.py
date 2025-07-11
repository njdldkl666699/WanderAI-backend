from fastapi import APIRouter

from common.log import log
from common.util import JwtUtil
from model.dto import UserLoginDTO
from model.entity import User
from model.result import Result
from model.vo import UserLoginVO
from server.service import UserService

router = APIRouter(prefix="/user")


@router.post("/login")
async def login(userLoginDTO: UserLoginDTO):
    log.info(f"用户登录: {userLoginDTO.name}")
    user: User = await UserService.login(userLoginDTO)

    # 登录成功后，生成jwt令牌
    token = JwtUtil.create_JWT({"user_id": user.id})
    userLoginVO = UserLoginVO(**dict(user), token=token)

    return Result.success(userLoginVO)


@router.get("/")
async def listUsers():
    log.info("获取用户列表")
    userList: list[User] = await UserService.list()
    return Result.success(userList)
