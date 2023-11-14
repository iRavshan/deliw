from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select
from data.models import Order, create_engine


class OrderRepository:
    def __init__(self):
        self.engine = create_engine()
        self.Session = sessionmaker(bind=self.engine)

    def create(self, order) -> Order:
        with self.Session() as session:
            session.add(order)
            session.commit()
            return user