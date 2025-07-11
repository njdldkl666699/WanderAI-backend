from fastapi import APIRouter

from common.log import log
from model.dto import StudentDTO
from model.entity import Student
from model.result import Result
from server.service import StudentService

router = APIRouter(prefix="/student")


@router.get("/")
async def hello_world():
    log.info("请求Hello World")
    return Result.success("Hello, World!")


@router.get("/{stu_id}")
async def get_student(stu_id: str, name: str | None = None):
    log.info(f"获取学生信息: ID={stu_id}, 姓名={name}")
    student: Student | None = await StudentService.get_student(stu_id, name)
    return Result.success(student)


@router.post("/")
async def post_student(student: StudentDTO):
    log.info(f"创建学生信息: {student}")
    await StudentService.create_student(student)
    return Result.success()
