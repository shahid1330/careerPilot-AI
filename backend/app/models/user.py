"""
User Model
Defines the User and UserRole tables
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.base import Base


class User(Base):
    """
    User model for authentication and user management
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    full_name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"


class UserRole(Base):
    """
    User Role model for role-based access control
    """
    __tablename__ = "user_roles"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_name = Column(String, nullable=False)
    duration_days = Column(
        Integer,
        nullable=False,
        default=365,
        server_default="365"
    )
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="roles")
    roadmaps = relationship("Roadmap", back_populates="user_role", cascade="all, delete-orphan")
    daily_plans = relationship("DailyPlan", back_populates="user_role", cascade="all, delete-orphan")
    mock_tests = relationship("MockTest", back_populates="user_role", cascade="all, delete-orphan")
    interview_sessions = relationship("InterviewSession", back_populates="user_role", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<UserRole(id={self.id}, user_id={self.user_id}, role={self.role_name})>"
