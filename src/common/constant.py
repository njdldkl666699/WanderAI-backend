class JwtConstant:
    """JWT常量类"""

    ADMIN_ID = "admin_id"
    ACCOUNT_ID = "account_id"
    EXPIRATION = "exp"


class MessageConstant:
    """消息常量类"""

    USER_NOT_FOUND = "用户未找到"
    ADMIN_NOT_FOUND = "管理员未找到"
    USER_ALREADY_EXISTS = "用户已存在"
    PASSWORD_ERROR = "密码错误"
    PLEASE_LOGIN = "请先登录"
    JWT_INVALID_OR_EXPIRED = "JWT无效或已过期"
    MODEL_NOT_FOUND = "模型未找到"
    MODEL_CANNOT_BE_EMPTY = "模型名称不能为空"
    SESSION_NOT_FOUND = "会话未找到"
    MESSAGE_CANNOT_BE_EMPTY = "消息内容不能为空"
    IMAGE_CANNOT_BE_EMPTY = "图片URL不能为空"
    MESSAGE_LIST_IS_EMPTY = "消息列表为空"
    UPLOAD_FAILED = "文件上传失败"
