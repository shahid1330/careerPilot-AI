"""
Phase 6B: Career Intelligence Engine
Models for career DNA, skill graphs, forecasts, and AI coaching
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.base import Base


class CareerDNAProfile(Base):
    """
    Career DNA Profile - User's learning and problem-solving characteristics
    """
    __tablename__ = "career_dna_profiles"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_role_id = Column(Integer, ForeignKey("user_roles.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    # DNA Dimensions (0.0 to 1.0)
    logical_ability = Column(Float, nullable=False, default=0.5)
    problem_solving = Column(Float, nullable=False, default=0.5)
    speed = Column(Float, nullable=False, default=0.5)
    consistency = Column(Float, nullable=False, default=0.5)
    learning_efficiency = Column(Float, nullable=False, default=0.5)
    
    # Calculated overall score
    overall_score = Column(Float, nullable=False, default=0.5)
    
    # DNA insights
    strengths = Column(JSON, nullable=True)  # ['Fast learner', 'Consistent performer']
    improvement_areas = Column(JSON, nullable=True)  # ['Logic building', 'Speed']
    personality_type = Column(String, nullable=True)  # 'Analytical Thinker', 'Quick Learner'
    
    # Metadata
    calculated_at = Column(DateTime, server_default=func.now())
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user_role = relationship("UserRole", foreign_keys=[user_role_id])
    
    def __repr__(self):
        return f"<CareerDNAProfile(id={self.id}, overall_score={self.overall_score})>"


class SkillGraph(Base):
    """
    Skill Graph - Network of skills with mastery levels
    """
    __tablename__ = "skill_graphs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_role_id = Column(Integer, ForeignKey("user_roles.id", ondelete="CASCADE"), nullable=False)
    
    # Skill details
    skill_name = Column(String, nullable=False)
    skill_category = Column(String, nullable=False)  # 'technical', 'soft', 'domain'
    
    # Mastery level (0.0 to 1.0)
    mastery_level = Column(Float, nullable=False, default=0.0)
    
    # Graph metrics
    node_weight = Column(Float, nullable=False, default=0.5)  # Importance in career
    connections = Column(JSON, nullable=True)  # Related skills ['React', 'JavaScript']
    
    # Learning data
    first_encountered = Column(DateTime, server_default=func.now())
    last_practiced = Column(DateTime, nullable=True)
    practice_count = Column(Integer, nullable=False, default=0)
    
    # Trend
    trend = Column(String, nullable=False, default='stable')  # 'improving', 'declining', 'stable'
    
    # Relationships
    user_role = relationship("UserRole", foreign_keys=[user_role_id])
    
    def __repr__(self):
        return f"<SkillGraph(id={self.id}, skill={self.skill_name}, mastery={self.mastery_level})>"


class CareerForecast(Base):
    """
    Career Forecast - Predictions based on learning data
    """
    __tablename__ = "career_forecasts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_role_id = Column(Integer, ForeignKey("user_roles.id", ondelete="CASCADE"), nullable=False)
    
    # Readiness scores (0.0 to 1.0)
    internship_readiness = Column(Float, nullable=False, default=0.0)
    placement_readiness = Column(Float, nullable=False, default=0.0)
    project_readiness = Column(Float, nullable=False, default=0.0)
    
    # Estimated timeline
    estimated_days_to_internship = Column(Integer, nullable=True)
    estimated_days_to_placement = Column(Integer, nullable=True)
    
    # Best fit roles
    best_fit_roles = Column(JSON, nullable=True)  # [{'role': 'Frontend Dev', 'match': 0.85}]
    
    # Predictions
    predicted_salary_range = Column(String, nullable=True)  # '6-8 LPA'
    success_probability = Column(Float, nullable=False, default=0.5)
    
    # AI insights
    forecast_summary = Column(Text, nullable=True)
    recommended_actions = Column(JSON, nullable=True)  # ['Focus on DSA', 'Build projects']
    
    # Metadata
    generated_at = Column(DateTime, server_default=func.now())
    valid_until = Column(DateTime, nullable=True)
    
    # Relationships
    user_role = relationship("UserRole", foreign_keys=[user_role_id])
    
    def __repr__(self):
        return f"<CareerForecast(id={self.id}, placement_readiness={self.placement_readiness})>"


class AICoachingSession(Base):
    """
    AI Coach - Weekly strategy and personalized guidance
    """
    __tablename__ = "ai_coaching_sessions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_role_id = Column(Integer, ForeignKey("user_roles.id", ondelete="CASCADE"), nullable=False)
    
    # Session details
    session_date = Column(DateTime, server_default=func.now())
    week_number = Column(Integer, nullable=False)
    
    # Weekly strategy
    weekly_focus = Column(JSON, nullable=True)  # ['Data Structures', 'System Design']
    priority_topics = Column(JSON, nullable=True)  # [{'topic': 'Binary Trees', 'reason': ''}]
    
    # Learning roadmap
    this_week_goals = Column(JSON, nullable=True)  # ['Complete 10 DSA problems', 'Build project']
    next_week_preview = Column(JSON, nullable=True)
    
    # Performance analysis
    last_week_progress = Column(Text, nullable=True)
    strengths_identified = Column(JSON, nullable=True)
    gaps_identified = Column(JSON, nullable=True)
    
    # Recommendations
    study_plan = Column(Text, nullable=True)
    resource_recommendations = Column(JSON, nullable=True)  # [{'type': 'video', 'link': ''}]
    practice_recommendations = Column(JSON, nullable=True)
    
    # Motivational content
    encouragement_message = Column(Text, nullable=True)
    milestone_celebration = Column(Text, nullable=True)
    
    # Relationships
    user_role = relationship("UserRole", foreign_keys=[user_role_id])
    
    def __repr__(self):
        return f"<AICoachingSession(id={self.id}, week={self.week_number})>"


class LearningVelocity(Base):
    """
    Learning Velocity - Tracks learning speed and patterns
    """
    __tablename__ = "learning_velocity"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_role_id = Column(Integer, ForeignKey("user_roles.id", ondelete="CASCADE"), nullable=False)
    
    # Velocity metrics
    topics_per_week = Column(Float, nullable=False, default=0.0)
    concepts_mastered_per_day = Column(Float, nullable=False, default=0.0)
    average_retention_rate = Column(Float, nullable=False, default=0.0)
    
    # Learning patterns
    peak_learning_hours = Column(JSON, nullable=True)  # ['9-11 AM', '3-5 PM']
    best_learning_days = Column(JSON, nullable=True)  # ['Monday', 'Wednesday']
    preferred_learning_mode = Column(String, nullable=True)  # 'video', 'reading', 'practice'
    
    # Engagement
    daily_streak = Column(Integer, nullable=False, default=0)
    longest_streak = Column(Integer, nullable=False, default=0)
    total_learning_hours = Column(Float, nullable=False, default=0.0)
    
    # Velocity trend
    velocity_trend = Column(String, nullable=False, default='stable')  # 'accelerating', 'stable', 'slowing'
    velocity_score = Column(Float, nullable=False, default=0.5)  # 0.0 to 1.0
    
    # Metadata
    calculated_at = Column(DateTime, server_default=func.now())
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user_role = relationship("UserRole", foreign_keys=[user_role_id])
    
    def __repr__(self):
        return f"<LearningVelocity(id={self.id}, velocity_score={self.velocity_score})>"
