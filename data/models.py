from datetime import datetime, timedelta
from loader import db_engine
import pytz
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import List
from typing import Optional
from uuid import UUID, uuid4 


class Base(DeclarativeBase):
    pass


class User(Base):
   __tablename__ ='users' 
   tgId: Mapped[str] = mapped_column(primary_key = True)
   firstname: Mapped[Optional[str]] 
   latitude: Mapped[Optional[float]]
   longitude: Mapped[Optional[float]]
   phone: Mapped[Optional[str]]
   created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow() + timedelta(hours=5))
   is_registered: Mapped[bool] = mapped_column(default=False)
   orders: Mapped[List["Order"]] = relationship(back_populates="user")


class Order(Base):
    __tablename__="orders"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4())
    user_id: Mapped[str] = mapped_column(ForeignKey("users.tgId"))
    user: Mapped["User"] = relationship(back_populates="orders")
    numbers: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(pytz.timezone('Asia/Tashkent')))


def migrate_data():
    Base.metadata.create_all(bind=db_engine)
