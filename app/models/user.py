from sqlalchemy import (
    Column,
    String,
    func,
    DateTime,
    Boolean,
    Float,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.database.base_class import Base
from datetime import datetime
from app.models.plan import Plans  # noqa
import pytz


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    email = Column(String, unique=True)
    password = Column(String(150))
    date_created = Column(DateTime(timezone=True), default=func.now())
    verified = Column(Boolean(False), default=False)
    balance = Column(Float, default=0)
    address = Column(String(150))
    user_ref_code = Column(String(150), unique=True)  # to be implemented
    upline_ref_code = Column(String(150))
    is_admin = Column(Boolean, default=False)
    last_login = Column(
        DateTime(timezone=True),
        default=datetime.now(pytz.UTC),
    )
    plans = relationship("Plans", backref="owner", passive_deletes=True)
    payment_detail = relationship("Payment_Details", uselist=False)


class Payment_Details(Base):  # type: ignore
    __tablename__ = "payment_details"

    id = Column(Integer, primary_key=True)
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    network = Column(String(150), default="Binance Smart Chain")
    wallet_address = Column(String(150))
    coin = Column(String(150), default="USDT")
