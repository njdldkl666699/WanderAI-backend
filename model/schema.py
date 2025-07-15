from sqlalchemy import DATETIME, INT, VARCHAR, Column, Null
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "user"

    id = Column(INT, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(20), nullable=False)
    password = Column(VARCHAR(36), default=Null)
    create_time = Column(DATETIME, default=Null)
