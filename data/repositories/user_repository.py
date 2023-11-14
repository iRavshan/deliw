from sqlalchemy.orm import Session
from sqlalchemy import select
from data.models import User
from loader import db_engine

class UserRepository:
    def __init__(self):
        self.session = Session(bind=db_engine)

    def find_by_id(self, userId: str) -> User:
        stmt = select(User).where(User.tgId == str(userId))
        user = self.session.scalars(stmt).one_or_none()
        return user

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        return user
    
    def update(self, userId: str, user: User):
        stmt = select(User).where(User.tgId == str(userId))
        ex_user = self.session.scalars(stmt).one()
        if ex_user:
            ex_user.firstname = user.firstname
            ex_user.latitude = user.latitude
            ex_user.longitude = user.longitude
            ex_user.phone = user.phone
            ex_user.is_registered = True
            self.session.commit()
            return ex_user
        else:
            return None