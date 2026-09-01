from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text
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

    scenario_type = Column(String)

    expected_sequence = Column(JSON)

    score = Column(Float)

    step_results = Column(JSON)

    completed_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sessions")

    gaze_events = relationship("GazeEvent", back_populates="session")

    coaching_report = relationship("CoachingReport", uselist=False, back_populates="session")


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


class CoachingReport(Base) :

    __tablename__ = "coaching_reports"

    id = Column(Integer, primary_key=True)

    session_id = Column(Integer, ForeignKey("sessions.id"), unique=True)

    summary = Column(Text)

    strengths = Column(JSON)

    areas_to_improve = Column(JSON)

    per_check_notes = Column(JSON)

    overall_score = Column(Float)

    model = Column(String)

    raw_response = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("Session", back_populates="coaching_report")





