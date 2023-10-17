from sqlalchemy import (
    Boolean,
    Column,
    String,
    DateTime,
    func,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import relationship
from app.database.base_class import Base


class TWCPosts(Base):  # type: ignore
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(300), nullable=False)
    category = Column(String(150), nullable=False)
    content = Column(String, nullable=False)
    thumbnail = Column(String(255), nullable=False, unique=True)
    tags = Column(String(255), nullable=False)
    date_created = Column(DateTime(timezone=True), default=func.now())


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    content = Column(String(300), nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    read = Column(Boolean, default=False)
    ower = relationship("Users", backref="notifications", passive_deletes=True)
