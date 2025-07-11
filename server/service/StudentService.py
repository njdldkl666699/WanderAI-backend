from common.constant.MessageConstant import (
    STUDENT_ALREADY_EXISTS,
    STUDENT_CANNOT_BE_EMPTY,
)
from common.exception import StudentAlreadyExistsException, StudentNotFoundException
from model.dto import StudentDTO
from model.entity import Student
from server.mapper.StudentMapper import get_student_by_query, insert_student


async def get_student(stu_id: str, name: str | None = None) -> Student | None:
    """获取学生信息"""
    if not stu_id or stu_id.strip() == "":
        raise StudentNotFoundException(STUDENT_CANNOT_BE_EMPTY)

    student_data = await get_student_by_query(stu_id, name)
    return student_data


async def create_student(student_dto: StudentDTO) -> None:
    """创建学生"""
    id = student_dto.ID
    name = student_dto.name
    if not id or id.strip() == "":
        raise StudentNotFoundException(STUDENT_CANNOT_BE_EMPTY)

    if not name or name.strip() == "":
        raise StudentNotFoundException(STUDENT_CANNOT_BE_EMPTY)

    student_db = await get_student_by_query(id)
    if student_db:
        raise StudentAlreadyExistsException(STUDENT_ALREADY_EXISTS)

    await insert_student(student_dto)
