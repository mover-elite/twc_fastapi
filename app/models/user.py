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
    # Bank Details
    bank_name = Column(String(150))
    bank_id = Column(String(20))
    bank_account = Column(String(20))
    account_name = Column(String(150))
    # Wallet Address Details
    network = Column(String(150))
    wallet_address = Column(String(150))
    coin = Column(String(150))
    # owner = relationship(
    #     "User",
    #     passive_deletes=True,
    #     uselist=False,
    # )
class TWCPosts(Base):  # type: ignore
    id = Column(Integer, primary_key=True)
    title = Column(String(300), nullable=False)
    category = Column(String(150), nullable=False)
    content = Column(String, nullable=False)
    thumbnail = Column(String(255), nullable=False, unique=True)
    tags = Column(String(255), nullable=False)
    date_created = Column(DateTime(timezone=True), default=func.now())

class Notification(Base):
    id = Column(Integer, primary_key=True)
    content = Column(String(300), nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    read = Column(Boolean, default=False)
    ower = relationship("Users", backref="notifications", passive_deletes=True)
