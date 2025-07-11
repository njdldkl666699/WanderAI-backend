from sqlalchemy import select

from common.context import BaseContext
from model.dto import StudentDTO
from model.entity import Student
from model.schema import StudentModel


async def get_students_by_name(name: str) -> list[Student]:
    db = BaseContext.get_db_session()
    stmt = select(StudentModel).where(StudentModel.name.like(f"%{name}%"))
    result = await db.execute(stmt)
    results = result.scalars().all()
    return [Student.model_validate(student) for student in results]


async def get_student_by_query(id: str, name: str | None = None) -> Student | None:
    db = BaseContext.get_db_session()
    stmt = select(StudentModel).where(StudentModel.ID == id)
    if name:
        stmt = stmt.where(StudentModel.name.like(f"%{name}%"))

    result = await db.execute(stmt)
    student_model = result.scalar_one_or_none()
    return Student.model_validate(student_model) if student_model else None


async def insert_student(student_data: StudentDTO) -> None:
    db = BaseContext.get_db_session()

    # 使用 ORM 模型插入数据
    student_model = StudentModel(
        ID=student_data.ID,
        name=student_data.name,
        dept_name=student_data.dept_name,
        tot_cred=student_data.tot_cred,
    )

    db.add(student_model)
    await db.commit()
    # # 刷新对象以获取数据库生成的值，主键可以通过刷新获取
    # await db.refresh(student_model)
