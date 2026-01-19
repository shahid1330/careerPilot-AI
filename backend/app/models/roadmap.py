"""
Roadmap Models
Defines Roadmap, DailyPlan, and TopicProgress tables
"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.base import Base


class Roadmap(Base):
    """
    Roadmap model for career learning paths
    """
    __tablename__ = "roadmaps"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_role_id = Column(Integer, ForeignKey("user_roles.id", ondelete="CASCADE"), nullable=False)
    roadmap_text = Column(Text, nullable=False)
    generated_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user_role = relationship("UserRole", back_populates="roadmaps")
    
    def __repr__(self):
        return f"<Roadmap(id={self.id}, user_role_id={self.user_role_id})>"


class DailyPlan(Base):
    """
    Daily Plan model for daily learning tasks
    """
    __tablename__ = "daily_plans"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_role_id = Column(Integer, ForeignKey("user_roles.id", ondelete="CASCADE"), nullable=False)
    day_number = Column(Integer, nullable=False)
    topic = Column(Text, nullable=False)
    estimated_hours = Column(Integer, nullable=False)
    
    # Relationships
    user_role = relationship("UserRole", back_populates="daily_plans")
    topic_progress = relationship("TopicProgress", back_populates="daily_plan", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<DailyPlan(id={self.id}, user_role_id={self.user_role_id}, day={self.day_number})>"


class TopicProgress(Base):
    """
    Topic Progress model for tracking learning progress
    """
    __tablename__ = "topic_progress"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    daily_plan_id = Column(Integer, ForeignKey("daily_plans.id", ondelete="CASCADE"), nullable=False)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    daily_plan = relationship("DailyPlan", back_populates="topic_progress")
    
    def __repr__(self):
        return f"<TopicProgress(id={self.id}, daily_plan_id={self.daily_plan_id}, completed={self.is_completed})>"
