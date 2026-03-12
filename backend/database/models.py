from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime 

from .connection import Base 

class User(Base) :

    __tablename__ = "users"

    id = Column(Integer,primary_key=True)

    email = Column(String, unique=True, index=True)

    password_hash = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("Session", back_populates="user")


class Session(Base) :

    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    scenario = Column(String)

    score = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sessions")

    gaze_events = relationship("GazeEvent", back_populates="session")


class GazeEvent(Base) :

    __tablename__ = "gaze_events"

    id = Column(Integer, primary_key=True)

    session_id = Column(Integer, ForeignKey("sessions.id"))

    pose = Column(String)

    yaw = Column(Float)

    pitch = Column(Float)

    duration = Column(Float)

    timestamp = Column(DateTime, default=datetime.utcnow)

    extra_data = Column(JSON)

    session = relationship("Session", back_populates="gaze_events")





