import random
import string

from wanderai.common.constant import JwtConstant, MessageConstant
from wanderai.common.context import BaseContext
from wanderai.common.exception import PasswordErrorException, UserNotFoundException
from wanderai.common.util import JwtUtil
from wanderai.model.dto import UserLoginDTO, UserRegisterDTO
from wanderai.model.entity import User
from wanderai.model.vo import UserLoginVO, UserRegisterVO
from wanderai.server.mapper import UserMapper


def generate_random_account_id() -> str:
    """生成一个随机的账号ID"""
    length = random.randint(6, 10)  # 随机长度 6-10
    chars = string.digits  # 数字
    return "".join(random.choices(chars, k=length))  # 随机生成


async def login(userLoginDTO: UserLoginDTO) -> UserLoginVO:
    """用户登录"""
    account_id = userLoginDTO.account_id
    password = userLoginDTO.password

    user = await UserMapper.get_user_by_account_id(account_id)
    # 检查用户是否存在
    if not user:
        raise UserNotFoundException(MessageConstant.USER_NOT_FOUND)

    # 密码比对
    if user.password != password:
        raise PasswordErrorException(MessageConstant.PASSWORD_ERROR)

    # 登录成功后，生成jwt令牌
    token = JwtUtil.create_JWT({JwtConstant.ACCOUNT_ID: user.account_id})
    userLoginVO = UserLoginVO(token=token, nickname=user.nickname)

    return userLoginVO


async def register(userRegisterDTO: UserRegisterDTO) -> UserRegisterVO:
    """用户注册"""
    nickname = userRegisterDTO.nickname
    password = userRegisterDTO.password

    while True:
        # 随机生成账号
        account_id = generate_random_account_id()

        existing_user = await UserMapper.get_user_by_account_id(account_id)
        if existing_user:
            # 用户存在，重新创建账号
            continue

        # 将新用户插入数据库中
        new_user = User(nickname=nickname, account_id=account_id, password=password)
        await UserMapper.create_user(new_user)

        # 创建VO
        userRegisterVO = UserRegisterVO(account_id=account_id)
        return userRegisterVO


async def update(new_nickname: str) -> None:
    """更新用户昵称"""

    # 获取账号
    account_id = BaseContext.get_account_id()
    if not account_id:
        raise UserNotFoundException(MessageConstant.USER_NOT_FOUND)

    await UserMapper.update_nickname_by_account_id(account_id, new_nickname)
