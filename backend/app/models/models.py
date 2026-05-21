from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.models.base import Base


class FriendshipStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    openid = Column(String(100), unique=True, index=True)
    nickname = Column(String(50), default="")
    avatar = Column(String(500), default="")
    daily_goal = Column(Integer, default=2000)
    created_at = Column(DateTime, default=datetime.utcnow)

    records = relationship("WaterRecord", back_populates="user")
    reminders = relationship("ReminderSetting", back_populates="user")


class WaterRecord(Base):
    __tablename__ = "water_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="records")


class Friendship(Base):
    __tablename__ = "friendships"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    friend_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(FriendshipStatus), default=FriendshipStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", foreign_keys=[user_id])
    friend = relationship("User", foreign_keys=[friend_id])


class ReminderSetting(Base):
    __tablename__ = "reminder_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    times = Column(String(500), default="")
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reminders")
