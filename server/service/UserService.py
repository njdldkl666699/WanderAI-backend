from common.constant.MessageConstant import PASSWORD_ERROR, USER_NOT_FOUND
from common.exception import PasswordErrorException, UserNotFoundException
from model.dto import UserLoginDTO
from model.entity import User
from server.mapper import UserMapper


async def login(userLoginDTO: UserLoginDTO) -> User:
    name = userLoginDTO.name
    password = userLoginDTO.password

    user: User | None = await UserMapper.get_user_by_name(name)
    if not user:
        raise UserNotFoundException(USER_NOT_FOUND)

    # 密码比对
    if user.password != password:
        raise PasswordErrorException(PASSWORD_ERROR)

    return user


async def list() -> list[User]:
    userList = await UserMapper.list()
    if not userList:
        return []
    return userList
