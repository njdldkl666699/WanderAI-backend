from common.constant import JwtConstant, MessageConstant
from common.exception import AdminNotFoundException, PasswordErrorException
from common.util import JwtUtil
from model.dto import AdminLoginDTO, DeleteAccountDTO, DeleteSuggestionDTO
from model.vo import AdminLoginVO, SuggestionVO, UserAccountVO
from server.mapper import AdminMapper, SuggestionMapper


async def login(adminLoginDTO: AdminLoginDTO) -> AdminLoginVO:
    """管理员登录"""
    admin_id = adminLoginDTO.admin_id
    password = adminLoginDTO.password

    admin = await AdminMapper.get_admin_by_admin_id(admin_id)
    # 检查管理员是否存在
    if not admin:
        raise AdminNotFoundException(MessageConstant.ADMIN_NOT_FOUND)

    # 密码比对
    if admin.password != password:
        raise PasswordErrorException(MessageConstant.PASSWORD_ERROR)

    # 登录成功后，生成jwt令牌
    token = JwtUtil.create_JWT({JwtConstant.ADMIN_ID: admin.admin_id})
    adminLoginVO = AdminLoginVO(token=token)
    # 返回管理员登录VO
    return adminLoginVO


async def list_users() -> list[UserAccountVO]:
    """列出所有用户"""
    users = await AdminMapper.list_users()
    return [UserAccountVO(account_id=user.account_id, nickname=user.nickname) for user in users]


async def get_acount(account_id) -> UserAccountVO:
    """查找具体用户"""
    user = await AdminMapper.get_account(account_id)
    return UserAccountVO(account_id=user.account_id, nickname=user.nickname)


async def delete_account(deleteAccountDTO: DeleteAccountDTO):
    """注销用户"""
    account_id = deleteAccountDTO.account_id
    await AdminMapper.delete_account(account_id)


async def get_suggestion(account_id: str) -> list[SuggestionVO]:
    """查找用户建议"""
    suggestion = await SuggestionMapper.get_suggestion(account_id)
    return [
        SuggestionVO(id=suggest.id, account_id=suggest.account_id, message=suggest.message)  # type: ignore
        for suggest in suggestion
    ]


async def get_all_suggestion() -> list[SuggestionVO]:
    """查找所有用户建议"""
    suggestion = await SuggestionMapper.get_all_suggestion()
    return [
        SuggestionVO(id=suggest.id, account_id=suggest.account_id, message=suggest.message)  # type: ignore
        for suggest in suggestion
    ]


async def delete_suggestion(deleteSuggestionDTO: DeleteSuggestionDTO):
    """删除用户建议"""
    id = deleteSuggestionDTO.id
    await SuggestionMapper.delete_suggestion(id)
