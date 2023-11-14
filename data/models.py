import sqlalchemy as orm
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime

HOST = "viaduct.proxy.rlwy.net"
PORT = "58784"
USER = "postgres"
PASSWORD = "E-GG32f2A5BfF3DCfG-dG3D3*Ef6f-g4"
DB_NAME = "railway"

class Base(DeclarativeBase):
    pass


class User(Base):
   __tablename__ ='users' 
   tgId: Mapped[str] = mapped_column(primary_key = True)
   firstname: Mapped[Optional[str]] 
   address: Mapped[Optional[str]]
   phone: Mapped[Optional[str]]
   created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
   is_registered: Mapped[bool] = mapped_column(default=False)
   orders: Mapped[List["Order"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Order(Base):
    __tablename__="orders"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.tgId"))
    user = relationship("User", back_populates="orders")
    numbers: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())


def create_engine() -> None:
    connection = f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'
    engine = orm.create_engine(connection)


def create_tables() -> None:
    engine = create_engine()
    Base.metadata.create_all(engine)
