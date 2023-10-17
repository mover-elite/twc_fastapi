from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    DateTime,
    String,
    Integer,
    ForeignKey,
    Boolean,
    Float,
)
from sqlalchemy.orm import relationship
from app.database.base_class import Base


class Plans(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True)
    plan_type_id = Column(
        Integer, ForeignKey("plan.id", ondelete="CASCADE"), nullable=False
    )

    duration = Column(Integer, nullable=False)

    date_created = Column(DateTime(timezone=True), default=func.now())
    start_date = Column(DateTime(timezone=True))

    date_completed = Column(DateTime(timezone=True))
    state = Column(String(100), default="pending")
    trxId = Column(String(300), nullable=False, unique=True)
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    plan_type = relationship("Plan", uselist=False, passive_deletes=True)


class Plan(Base):
    __tablename__ = "plan"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    price = Column(Float, nullable=False)
    category = Column(String(255), nullable=False)
    trading_idea = Column(Boolean, default=True)
    live_support = Column(Boolean, default=True)
    state = Column(String, default="active", nullable=False)
