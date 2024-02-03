from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base_class import Base
import shortuuid


def gen_id():
    return shortuuid.random(length=8)


class Plans(Base):
    __tablename__ = "plans"

    id = Column(String, primary_key=True, default=gen_id)
    amount = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)

    date_created = Column(DateTime(timezone=True), default=func.now())
    start_date = Column(DateTime(timezone=True))
    date_completed = Column(DateTime(timezone=True))

    status = Column(String(100), default="pending")
    trx_id = Column(String(300), nullable=False, unique=True)
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    payouts = relationship("PayOut", backref="plan", passive_deletes=True)


class PayOut(Base):
    __tablename__ = "payouts"

    id = Column(Integer, primary_key=True)
    plan_id = Column(String, ForeignKey("plans.id", ondelete="CASCADE"))
    amount = Column(Float, nullable=False)
    date = Column(DateTime(timezone=True), default=func.now())


# class Plan(Base):
#     __tablename__ = "plan"

#     id = Column(Integer, primary_key=True)
#     name = Column(String(255), nullable=False, unique=True)
#     price = Column(Float, nullable=False)
#     category = Column(String(255), nullable=False)
#     trading_idea = Column(Boolean, default=True)
#     live_support = Column(Boolean, default=True)
#     state = Column(String, default="active", nullable=False)
