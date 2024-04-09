from sqlalchemy.orm import Session
from sqlalchemy import select
from data.models import Order
from loader import db_engine


class OrderRepository:
    def __init__(self):
        self.session = Session(bind=db_engine)

    def create(self, order) -> Order:
        self.session.add(order)
        self.session.commit()
        return order
    
    def get_active_orders(self, user_id: str):
        stmt = select(Order).where(Order.user_id == user_id)
        orders = self.session.scalars(stmt).all()
        return orders