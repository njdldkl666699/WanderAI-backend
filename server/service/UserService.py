from common.constant.MessageConstant import PASSWORD_ERROR, USER_NOT_FOUND
from common.exception import PasswordErrorException, UserNotFoundException
from model.dto import UserLoginDTO, UserRegisterDTO,UserUpdateDTO
from model.entity import User
from server.mapper import UserMapper
from common.context import BaseContext
import random
import string

def generate_random_string():
    """生成一个随机的账号ID"""
    length = random.randint(12, 15)  # 随机长度 12-15
    chars = string.ascii_letters + string.digits  # 字母 + 数字
    return ''.join(random.choices(chars, k=length))  # 随机生成


async def login(userLoginDTO: UserLoginDTO) -> User:
    account_id = userLoginDTO.account_id
    password = userLoginDTO.password

    user: User | None = await UserMapper.get_user_by_account_id(account_id)
    if not user:
        raise UserNotFoundException(USER_NOT_FOUND)

    # 密码比对
    if user.password != password:
        raise PasswordErrorException(PASSWORD_ERROR)

    return user

async def register(userRegisterDTO: UserRegisterDTO) -> User:
    nickname = userRegisterDTO.nickname
    password = userRegisterDTO.password


    # 检查用户是否已存在
    while True:
        account_id = generate_random_string()
        existing_user: User | None = await UserMapper.get_user_by_account_id(account_id)
        if existing_user:
            raise UserNotFoundException(f"用户 {nickname} 已存在")
        else:
            # 创建新用户
            new_user = User(nickname=nickname, account_id=account_id, password=password)
            await UserMapper.create_user(new_user)
            return new_user

async def update(userUpdateDTO: UserUpdateDTO) -> User:
    """更新用户昵称"""
    new_nickname = userUpdateDTO.newNickname
    temp_account_id = BaseContext.get_user_account_id()
    if not temp_account_id:
        raise UserNotFoundException(USER_NOT_FOUND)
    user: User | None = await UserMapper.get_user_by_account_id(temp_account_id)
    if not user:
        raise UserNotFoundException(USER_NOT_FOUND)
    user.nickname = new_nickname
    await UserMapper.update_user_nickname(user.account_id, new_nickname)
    return user

async def list() -> list[User]:
    userList = await UserMapper.list()
    if not userList:
        return []
    return userList
