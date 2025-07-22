class AppException(Exception):
    """应用程序异常基类"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(AppException):
    """用户未找到异常"""


class UserAlreadyExistsException(AppException):
    """用户已存在异常"""


class AdminNotFoundException(AppException):
    """管理员未找到异常"""


class PasswordErrorException(AppException):
    """密码错误异常"""


class UnauthorizedException(AppException):
    """未授权异常"""


class ModelNotFoundException(AppException):
    """模型未找到异常"""


class SessionNotFoundException(AppException):
    """会话未找到异常"""


class MessageCannotBeEmptyException(AppException):
    """消息内容不能为空异常"""


class MessageListEmptyException(AppException):
    """消息列表为空异常"""
