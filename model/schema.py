from sqlalchemy import DATETIME, DECIMAL, INT, VARCHAR, Column, Null
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class StudentModel(Base):
    __tablename__ = "student"

    ID = Column(VARCHAR(5), primary_key=True)
    name = Column(VARCHAR(20), nullable=False)
    dept_name = Column(VARCHAR(20))
    tot_cred = Column(DECIMAL(3, 0))


class UserModel(Base):
    __tablename__ = "user"

    id = Column(INT, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(20), nullable=False)
    password = Column(VARCHAR(36), default=Null)
    create_time = Column(DATETIME, default=Null)
