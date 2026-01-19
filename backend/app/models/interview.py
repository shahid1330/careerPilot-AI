"""
Interview Models
Defines InterviewSession and InterviewFeedback tables
"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.base import Base


class InterviewSession(Base):
    """
    Interview Session model for mock interviews
    """
    __tablename__ = "interview_sessions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_role_id = Column(Integer, ForeignKey("user_roles.id", ondelete="CASCADE"), nullable=False)
    interview_date = Column(DateTime, server_default=func.now())
    duration_minutes = Column(Integer, nullable=False)
    
    # Relationships
    user_role = relationship("UserRole", back_populates="interview_sessions")
    feedback = relationship("InterviewFeedback", back_populates="interview_session", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<InterviewSession(id={self.id}, user_role_id={self.user_role_id})>"


class InterviewFeedback(Base):
    """
    Interview Feedback model for storing feedback after interviews
    """
    __tablename__ = "interview_feedback"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    interview_session_id = Column(Integer, ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=False)
    strengths = Column(Text, nullable=True)
    weaknesses = Column(Text, nullable=True)
    overall_score = Column(Integer, nullable=True)
    
    # Relationships
    interview_session = relationship("InterviewSession", back_populates="feedback")
    
    def __repr__(self):
        return f"<InterviewFeedback(id={self.id}, interview_session_id={self.interview_session_id}, score={self.overall_score})>"
