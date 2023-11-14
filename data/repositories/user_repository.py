from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select
from data.models import User, create_engine


class UserRepository:
    def __init__(self):
        self.engine = create_engine()
        self.Session = sessionmaker(bind=self.engine)

    def find_by_id(self, userId: str) -> User:
        with self.Session() as session:
            user = session.query(User).get(userId)
            return user

    def create(self, user: User) -> User:
        with self.Session() as session:
            session.add(user)
            session.commit()
            return user
    
    def update(self, userId, user: User):
        with self.Session() as session:
            ex_user = session.query(User).get(userId)
            if ex_user:
                ex_user.firstname = user.firstname
                ex_user.address = user.address
                ex_user.phone = user.phone
                ex_user.is_registered = True
                session.commit()
                return ex_user
            else:
                return None