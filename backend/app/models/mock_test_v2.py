"""
Phase 6A: Smart Weekly Mock Test & Evaluation System
Enhanced mock test models with MCQ and Coding sections
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.base import Base


class MockTestV2(Base):
    """
    Enhanced Mock Test model for Phase 6A
    Supports both MCQ and Coding sections
    """
    __tablename__ = "mock_tests_v2"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_role_id = Column(Integer, ForeignKey("user_roles.id", ondelete="CASCADE"), nullable=False)
    test_date = Column(DateTime, server_default=func.now())
    test_name = Column(String, nullable=False)
    test_type = Column(String, nullable=False)  # 'weekly', 'custom'
    
    # Topics used for this test (JSON array)
    topics_used = Column(JSON, nullable=False)  # ['React', 'Node.js', 'SQL']
    
    # Test configuration
    mcq_count = Column(Integer, nullable=False)  # 10, 15, or 20
    coding_count = Column(Integer, nullable=False)  # 2-4
    
    # Status
    status = Column(String, nullable=False, default='pending')  # 'pending', 'in_progress', 'completed'
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Time tracking
    time_limit_minutes = Column(Integer, nullable=False, default=60)
    time_taken_minutes = Column(Integer, nullable=True)
    
    # Relationships
    user_role = relationship("UserRole", foreign_keys=[user_role_id])
    questions = relationship("MockTestQuestion", back_populates="test", cascade="all, delete-orphan")
    attempts = relationship("MockTestAttempt", back_populates="test", cascade="all, delete-orphan")
    section_scores = relationship("MockTestSectionScore", back_populates="test", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<MockTestV2(id={self.id}, name={self.test_name}, status={self.status})>"


class MockTestQuestion(Base):
    """
    Individual questions for mock tests (MCQ + Coding)
    """
    __tablename__ = "mock_test_questions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    test_id = Column(Integer, ForeignKey("mock_tests_v2.id", ondelete="CASCADE"), nullable=False)
    
    # Question details
    question_type = Column(String, nullable=False)  # 'mcq' or 'coding'
    question_text = Column(Text, nullable=False)
    topic = Column(String, nullable=False)  # Which topic this question covers
    difficulty = Column(String, nullable=False)  # 'easy', 'medium', 'hard'
    
    # MCQ specific fields
    options = Column(JSON, nullable=True)  # ['Option A', 'Option B', 'Option C', 'Option D']
    correct_answer = Column(String, nullable=True)  # For MCQ: 'A', 'B', 'C', or 'D'
    
    # Coding specific fields
    test_cases = Column(JSON, nullable=True)  # [{'input': '', 'expected_output': ''}]
    starter_code = Column(Text, nullable=True)
    language = Column(String, nullable=True, default='python')  # Coding language for this question
    
    # Points
    points = Column(Integer, nullable=False, default=1)
    
    # Relationships
    test = relationship("MockTestV2", back_populates="questions")
    
    def __repr__(self):
        return f"<MockTestQuestion(id={self.id}, type={self.question_type}, topic={self.topic})>"


class MockTestAttempt(Base):
    """
    User's complete attempt for a mock test
    """
    __tablename__ = "mock_test_attempts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    test_id = Column(Integer, ForeignKey("mock_tests_v2.id", ondelete="CASCADE"), nullable=False)
    user_role_id = Column(Integer, ForeignKey("user_roles.id", ondelete="CASCADE"), nullable=False)
    
    # Attempt details
    attempt_number = Column(Integer, nullable=False, default=1)
    started_at = Column(DateTime, server_default=func.now())
    submitted_at = Column(DateTime, nullable=True)
    
    # Scores
    mcq_score = Column(Float, nullable=False, default=0.0)
    coding_score = Column(Float, nullable=False, default=0.0)
    total_score = Column(Float, nullable=False, default=0.0)
    
    # Analysis
    weak_topics = Column(JSON, nullable=True)  # ['React', 'SQL']
    strong_topics = Column(JSON, nullable=True)  # ['Node.js', 'Python']
    
    # AI feedback
    ai_feedback = Column(Text, nullable=True)
    improvement_plan = Column(Text, nullable=True)
    
    # Anti-cheat tracking
    violations_count = Column(Integer, nullable=False, default=0)
    violations_log = Column(JSON, nullable=True)  # [{'type': 'tab_switch', 'timestamp': '...'}]
    
    # Relationships
    test = relationship("MockTestV2", back_populates="attempts")
    user_role = relationship("UserRole", foreign_keys=[user_role_id])
    coding_submissions = relationship("CodingSubmission", back_populates="attempt", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<MockTestAttempt(id={self.id}, test_id={self.test_id}, total_score={self.total_score})>"


class MockTestSectionScore(Base):
    """
    Section-wise scoring breakdown
    """
    __tablename__ = "mock_test_section_scores"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    test_id = Column(Integer, ForeignKey("mock_tests_v2.id", ondelete="CASCADE"), nullable=False)
    attempt_id = Column(Integer, ForeignKey("mock_test_attempts.id", ondelete="CASCADE"), nullable=False)
    
    # Section details
    section_type = Column(String, nullable=False)  # 'mcq' or 'coding'
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False, default=0)
    incorrect_answers = Column(Integer, nullable=False, default=0)
    unanswered = Column(Integer, nullable=False, default=0)
    
    # Scoring
    score_obtained = Column(Float, nullable=False, default=0.0)
    max_score = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False, default=0.0)
    
    # Relationships
    test = relationship("MockTestV2", back_populates="section_scores")
    attempt = relationship("MockTestAttempt", foreign_keys=[attempt_id])
    
    def __repr__(self):
        return f"<MockTestSectionScore(id={self.id}, section={self.section_type}, score={score_obtained})>"


class CodingSubmission(Base):
    """
    Individual coding question submissions
    """
    __tablename__ = "coding_submissions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    attempt_id = Column(Integer, ForeignKey("mock_test_attempts.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("mock_test_questions.id", ondelete="CASCADE"), nullable=False)
    
    # Submission details
    code_submitted = Column(Text, nullable=False)
    language = Column(String, nullable=False, default='python')
    submitted_at = Column(DateTime, server_default=func.now())
    
    # Evaluation
    test_cases_passed = Column(Integer, nullable=False, default=0)
    total_test_cases = Column(Integer, nullable=False)
    execution_time_ms = Column(Integer, nullable=True)
    
    # Results
    is_correct = Column(Boolean, nullable=False, default=False)
    score_obtained = Column(Float, nullable=False, default=0.0)
    feedback = Column(Text, nullable=True)
    
    # Relationships
    attempt = relationship("MockTestAttempt", back_populates="coding_submissions")
    question = relationship("MockTestQuestion", foreign_keys=[question_id])
    
    def __repr__(self):
        return f"<CodingSubmission(id={self.id}, question_id={self.question_id}, passed={test_cases_passed}/{total_test_cases})>"


class UserPerformanceMetrics(Base):
    """
    User's overall performance analytics
    """
    __tablename__ = "user_performance_metrics"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_role_id = Column(Integer, ForeignKey("user_roles.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    # Overall stats
    total_tests_taken = Column(Integer, nullable=False, default=0)
    average_score = Column(Float, nullable=False, default=0.0)
    best_score = Column(Float, nullable=False, default=0.0)
    worst_score = Column(Float, nullable=False, default=0.0)
    
    # Improvement tracking
    score_trend = Column(JSON, nullable=True)  # [{'date': '', 'score': 0}]
    accuracy_improvement = Column(Float, nullable=False, default=0.0)
    
    # Topic analytics
    strong_areas = Column(JSON, nullable=True)  # [{'topic': 'React', 'accuracy': 0.85}]
    weak_areas = Column(JSON, nullable=True)  # [{'topic': 'SQL', 'accuracy': 0.45}]
    
    # Last updated
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user_role = relationship("UserRole", foreign_keys=[user_role_id])
    
    def __repr__(self):
        return f"<UserPerformanceMetrics(id={self.id}, avg_score={self.average_score})>"


class DailyQuote(Base):
    """
    Daily motivational quotes
    """
    __tablename__ = "daily_quotes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quote_text = Column(Text, nullable=False)
    author = Column(String, nullable=False)
    category = Column(String, nullable=False)  # 'motivation', 'success', 'learning'
    created_at = Column(DateTime, server_default=func.now())
    
    def __repr__(self):
        return f"<DailyQuote(id={self.id}, author={self.author})>"
