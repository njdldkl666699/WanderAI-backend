import uuid
from fastapi import APIRouter, UploadFile
from common.constant import MessageConstant
from common.log import log
from common.util import AliOssUtil
from model.result import Result

router = APIRouter(prefix="/upload")


@router.post("/")
async def upload_file(file: UploadFile):
    """上传文件"""
    log.info(f"上传文件: {file.filename}")
    try:
        original_filename = file.filename
        extension = None
        if original_filename:
            extension = original_filename.split(".")[-1]
        else:
            extension = ".png"

        # 构造新文件名
        filename = f"images/{uuid.uuid4()}.{extension}"
        # 上传到阿里云OSS
        file_content = await file.read()
        filepath = AliOssUtil.put_object(filename, file_content)
        return Result.success(filepath)
    except Exception as e:
        log.error(f"文件上传失败: {e}")

    return Result.error(MessageConstant.UPLOAD_FAILED)
