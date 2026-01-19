"""
Test Models
Defines MockTest and TestResult tables
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.base import Base


class MockTest(Base):
    """
    Mock Test model for assessments
    """
    __tablename__ = "mock_tests"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_role_id = Column(Integer, ForeignKey("user_roles.id", ondelete="CASCADE"), nullable=False)
    test_date = Column(DateTime, nullable=False)
    test_type = Column(String, nullable=False)
    
    # Relationships
    user_role = relationship("UserRole", back_populates="mock_tests")
    test_results = relationship("TestResult", back_populates="mock_test", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<MockTest(id={self.id}, user_role_id={self.user_role_id}, type={self.test_type})>"


class TestResult(Base):
    """
    Test Result model for storing user test attempts
    """
    __tablename__ = "test_results"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    mock_test_id = Column(Integer, ForeignKey("mock_tests.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, nullable=False)
    feedback = Column(Text, nullable=True)
    
    # Relationships
    mock_test = relationship("MockTest", back_populates="test_results")
    
    def __repr__(self):
        return f"<TestResult(id={self.id}, mock_test_id={self.mock_test_id}, score={self.score})>"
