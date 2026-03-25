"""
Phase 6B: Career Intelligence Engine
Pydantic schemas for career analytics and AI coaching
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# ==================== Career DNA Schemas ====================

class CareerDNADimensions(BaseModel):
    """Individual DNA dimensions"""
    logical_ability: float = Field(..., ge=0.0, le=1.0)
    problem_solving: float = Field(..., ge=0.0, le=1.0)
    speed: float = Field(..., ge=0.0, le=1.0)
    consistency: float = Field(..., ge=0.0, le=1.0)
    learning_efficiency: float = Field(..., ge=0.0, le=1.0)


class CareerDNAProfileResponse(BaseModel):
    """Complete Career DNA Profile"""
    user_role_id: int
    dimensions: CareerDNADimensions
    overall_score: float
    strengths: List[str]
    improvement_areas: List[str]
    personality_type: str
    calculated_at: datetime
    last_updated: datetime
    
    class Config:
        from_attributes = True


# ==================== Skill Graph Schemas ====================

class SkillNode(BaseModel):
    """Single skill in the graph"""
    skill_name: str
    skill_category: str
    mastery_level: float = Field(..., ge=0.0, le=1.0)
    node_weight: float
    connections: List[str]
    trend: str  # 'improving', 'declining', 'stable'
    practice_count: int
    last_practiced: Optional[datetime] = None


class SkillGraphResponse(BaseModel):
    """Complete skill graph for user"""
    user_role_id: int
    skills: List[SkillNode]
    total_skills: int
    average_mastery: float
    top_skills: List[str]
    skills_to_improve: List[str]


# ==================== Career Forecast Schemas ====================

class BestFitRole(BaseModel):
    """Role recommendation with match score"""
    role: str
    match_percentage: float = Field(..., ge=0.0, le=1.0)
    required_skills: List[str]
    missing_skills: List[str]
    estimated_days_to_ready: int


class CareerForecastResponse(BaseModel):
    """Career predictions and readiness"""
    user_role_id: int
    
    # Readiness scores
    internship_readiness: float = Field(..., ge=0.0, le=1.0)
    placement_readiness: float = Field(..., ge=0.0, le=1.0)
    project_readiness: float = Field(..., ge=0.0, le=1.0)
    
    # Timeline
    estimated_days_to_internship: Optional[int] = None
    estimated_days_to_placement: Optional[int] = None
    
    # Role recommendations
    best_fit_roles: List[BestFitRole]
    
    # Predictions
    predicted_salary_range: Optional[str] = None
    success_probability: float
    
    # AI insights
    forecast_summary: str
    recommended_actions: List[str]
    
    generated_at: datetime
    valid_until: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ==================== AI Coaching Schemas ====================

class WeeklyGoal(BaseModel):
    """Single goal for the week"""
    goal: str
    priority: str  # 'high', 'medium', 'low'
    estimated_hours: int


class ResourceRecommendation(BaseModel):
    """Learning resource"""
    type: str  # 'video', 'article', 'course', 'practice'
    title: str
    link: str
    duration_minutes: Optional[int] = None


class AICoachingResponse(BaseModel):
    """Weekly coaching session"""
    user_role_id: int
    session_date: datetime
    week_number: int
    
    # Weekly focus
    weekly_focus: List[str]
    priority_topics: List[Dict[str, str]]  # [{'topic': '', 'reason': ''}]
    
    # Goals
    this_week_goals: List[WeeklyGoal]
    next_week_preview: List[str]
    
    # Analysis
    last_week_progress: str
    strengths_identified: List[str]
    gaps_identified: List[str]
    
    # Recommendations
    study_plan: str
    resource_recommendations: List[ResourceRecommendation]
    practice_recommendations: List[str]
    
    # Motivation
    encouragement_message: str
    milestone_celebration: Optional[str] = None
    
    class Config:
        from_attributes = True


# ==================== Learning Velocity Schemas ====================

class LearningPattern(BaseModel):
    """User's learning patterns"""
    peak_learning_hours: List[str]
    best_learning_days: List[str]
    preferred_learning_mode: str


class LearningVelocityResponse(BaseModel):
    """Learning speed and engagement metrics"""
    user_role_id: int
    
    # Velocity metrics
    topics_per_week: float
    concepts_mastered_per_day: float
    average_retention_rate: float
    
    # Patterns
    learning_patterns: LearningPattern
    
    # Engagement
    daily_streak: int
    longest_streak: int
    total_learning_hours: float
    
    # Trend
    velocity_trend: str  # 'accelerating', 'stable', 'slowing'
    velocity_score: float = Field(..., ge=0.0, le=1.0)
    
    calculated_at: datetime
    last_updated: datetime
    
    class Config:
        from_attributes = True


# ==================== Combined Intelligence Dashboard ====================

class CareerIntelligenceDashboard(BaseModel):
    """Complete career intelligence overview"""
    career_dna: CareerDNAProfileResponse
    skill_graph: SkillGraphResponse
    forecast: CareerForecastResponse
    coaching: AICoachingResponse
    velocity: LearningVelocityResponse
    
    # Overall insights
    overall_readiness: float
    next_milestone: str
    days_to_milestone: int
