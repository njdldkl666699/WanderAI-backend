from common.constant import JwtConstant, MessageConstant
from common.exception import PasswordErrorException, AdminNotFoundException
from common.util import JwtUtil
from model.dto import AdminLoginDTO,DeleteAccountDTO,GetSuggestionDTO,DeleteSuggestionDTO,GetAccountDTO
from model.vo import AdminLoginVO,UserAccountVO,SuggestionVO
from server.mapper import AdminMapper


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
    token = JwtUtil.create_JWT({JwtConstant.ASMIN_ID: admin.admin_id})
    adminLoginVO = AdminLoginVO(token=token)
    # 返回管理员登录VO
    return adminLoginVO


async def list_users() -> list[UserAccountVO]:
    """列出所有用户"""
    users = await AdminMapper.list_users()
    return [UserAccountVO(account_id = user.account_id,nickname = user.nickname) for user in users]

async def get_acount(getAccountDTO:GetAccountDTO) ->UserAccountVO:
    """查找具体用户"""
    account_id = getAccountDTO.account_id
    user = await AdminMapper.get_account(account_id)
    return UserAccountVO(account_id = user.account_id,nickname = user.nickname)

async def delete_account(deleteAccountDTO: DeleteAccountDTO):
    """注销用户"""
    account_id = deleteAccountDTO.account_id
    await AdminMapper.delete_account(account_id)

async def get_suggestion(getSuggestion:GetSuggestionDTO) -> list[SuggestionVO]:
    """查找用户建议"""
    account_id=getSuggestion.account_id
    suggestion = await AdminMapper.get_suggestion(account_id)
    return [SuggestionVO(account_id=suggest.account_id,message=suggest.message)for suggest in suggestion]

async def get_all_suggestion() -> list[SuggestionVO]:
    """查找所有用户建议"""
    suggestion = await AdminMapper.get_all_suggestion()
    return [SuggestionVO(account_id=suggest.account_id,message=suggest.message)for suggest in suggestion]

async def delete_suggestion(deleteSuggestionDTO:DeleteSuggestionDTO):
    """删除用户建议"""
    id = deleteSuggestionDTO.id
    await AdminMapper.delete_suggestion(id)

