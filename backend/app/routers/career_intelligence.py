"""
Phase 6B: Career Intelligence API
Career DNA, Skill Graph, Forecasts, and AI Coaching
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Dict
from datetime import datetime, timedelta

from app.core.database import get_db
from app.utils.jwt import get_current_user
from app.models.user import User, UserRole
from app.models.roadmap import TopicProgress, DailyPlan
from app.models.mock_test_v2 import MockTestAttempt, UserPerformanceMetrics
from app.models.career_intelligence import (
    CareerDNAProfile, SkillGraph, CareerForecast,
    AICoachingSession, LearningVelocity
)
from app.schemas.career_intelligence_schemas import (
    CareerDNAProfileResponse, CareerDNADimensions,
    SkillGraphResponse, SkillNode,
    CareerForecastResponse, BestFitRole,
    AICoachingResponse, WeeklyGoal, ResourceRecommendation,
    LearningVelocityResponse, LearningPattern,
    CareerIntelligenceDashboard
)
from app.services.phase6_ai_service import phase6_ai_service

router = APIRouter(prefix="/career-intelligence", tags=["Career Intelligence"])


@router.get("/dna", response_model=CareerDNAProfileResponse)
async def get_career_dna(
    user_role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get or generate Career DNA Profile"""
    
    # Verify ownership
    user_role = db.query(UserRole).filter(
        UserRole.id == user_role_id,
        UserRole.user_id == current_user.id
    ).first()
    
    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    # Check if profile exists
    profile = db.query(CareerDNAProfile).filter(
        CareerDNAProfile.user_role_id == user_role_id
    ).first()
    
    if not profile:
        # Generate new DNA profile based on test performance
        profile = generate_career_dna(db, user_role_id)
    
    return CareerDNAProfileResponse(
        user_role_id=profile.user_role_id,
        dimensions=CareerDNADimensions(
            logical_ability=profile.logical_ability,
            problem_solving=profile.problem_solving,
            speed=profile.speed,
            consistency=profile.consistency,
            learning_efficiency=profile.learning_efficiency
        ),
        overall_score=profile.overall_score,
        strengths=profile.strengths or [],
        improvement_areas=profile.improvement_areas or [],
        personality_type=profile.personality_type or "Aspiring Professional",
        calculated_at=profile.calculated_at,
        last_updated=profile.last_updated
    )


@router.get("/skills", response_model=SkillGraphResponse)
async def get_skill_graph(
    user_role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get skill graph with mastery levels"""
    
    # Verify ownership
    user_role = db.query(UserRole).filter(
        UserRole.id == user_role_id,
        UserRole.user_id == current_user.id
    ).first()
    
    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    # Get or generate skill graph
    skills = db.query(SkillGraph).filter(
        SkillGraph.user_role_id == user_role_id
    ).all()
    
    if not skills:
        skills = generate_skill_graph(db, user_role_id)
    
    # Convert to response format
    skill_nodes = []
    total_mastery = 0
    
    for skill in skills:
        skill_nodes.append(SkillNode(
            skill_name=skill.skill_name,
            skill_category=skill.skill_category,
            mastery_level=skill.mastery_level,
            node_weight=skill.node_weight,
            connections=skill.connections or [],
            trend=skill.trend,
            practice_count=skill.practice_count,
            last_practiced=skill.last_practiced
        ))
        total_mastery += skill.mastery_level
    
    avg_mastery = total_mastery / len(skills) if skills else 0
    
    # Get top skills and skills to improve
    sorted_skills = sorted(skills, key=lambda x: x.mastery_level, reverse=True)
    top_skills = [s.skill_name for s in sorted_skills[:5]]
    skills_to_improve = [s.skill_name for s in sorted_skills[-5:] if s.mastery_level < 0.6]
    
    return SkillGraphResponse(
        user_role_id=user_role_id,
        skills=skill_nodes,
        total_skills=len(skills),
        average_mastery=round(avg_mastery, 2),
        top_skills=top_skills,
        skills_to_improve=skills_to_improve
    )


@router.get("/forecast", response_model=CareerForecastResponse)
async def get_career_forecast(
    user_role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get career readiness forecast and predictions"""
    
    # Verify ownership
    user_role = db.query(UserRole).filter(
        UserRole.id == user_role_id,
        UserRole.user_id == current_user.id
    ).first()
    
    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    # Get or generate forecast
    forecast = db.query(CareerForecast).filter(
        CareerForecast.user_role_id == user_role_id
    ).first()
    
    if not forecast or (forecast.valid_until and forecast.valid_until < datetime.utcnow()):
        # Generate new forecast
        forecast = generate_career_forecast(db, user_role_id, user_role.role_name)
    
    # Parse best fit roles
    best_fit_roles = []
    if forecast.best_fit_roles:
        for role_data in forecast.best_fit_roles:
            best_fit_roles.append(BestFitRole(
                role=role_data.get('role', ''),
                match_percentage=role_data.get('match', 0.0),
                required_skills=role_data.get('required_skills', []),
                missing_skills=role_data.get('missing_skills', []),
                estimated_days_to_ready=role_data.get('days', 30)
            ))
    
    return CareerForecastResponse(
        user_role_id=user_role_id,
        internship_readiness=forecast.internship_readiness,
        placement_readiness=forecast.placement_readiness,
        project_readiness=forecast.project_readiness,
        estimated_days_to_internship=forecast.estimated_days_to_internship,
        estimated_days_to_placement=forecast.estimated_days_to_placement,
        best_fit_roles=best_fit_roles,
        predicted_salary_range=forecast.predicted_salary_range,
        success_probability=forecast.success_probability,
        forecast_summary=forecast.forecast_summary,
        recommended_actions=forecast.recommended_actions or [],
        generated_at=forecast.generated_at,
        valid_until=forecast.valid_until
    )


@router.get("/coaching", response_model=AICoachingResponse)
async def get_ai_coaching(
    user_role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get AI coaching session with weekly strategy"""
    
    # Verify ownership
    user_role = db.query(UserRole).filter(
        UserRole.id == user_role_id,
        UserRole.user_id == current_user.id
    ).first()
    
    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    # Get latest coaching session
    coaching = db.query(AICoachingSession).filter(
        AICoachingSession.user_role_id == user_role_id
    ).order_by(desc(AICoachingSession.session_date)).first()
    
    # Check if we need a new session (weekly)
    if not coaching or (datetime.utcnow() - coaching.session_date).days >= 7:
        coaching = generate_coaching_session(db, user_role_id)
    
    # Parse goals
    this_week_goals = []
    if coaching.this_week_goals:
        for goal_data in coaching.this_week_goals:
            if isinstance(goal_data, dict):
                this_week_goals.append(WeeklyGoal(
                    goal=goal_data.get('goal', ''),
                    priority=goal_data.get('priority', 'medium'),
                    estimated_hours=goal_data.get('hours', 5)
                ))
    
    # Parse resources
    resource_recs = []
    if coaching.resource_recommendations:
        for res_data in coaching.resource_recommendations:
            if isinstance(res_data, dict):
                resource_recs.append(ResourceRecommendation(
                    type=res_data.get('type', 'article'),
                    title=res_data.get('title', ''),
                    link=res_data.get('link', '#'),
                    duration_minutes=res_data.get('duration')
                ))
    
    # Parse priority topics
    priority_topics = coaching.priority_topics or []
    
    return AICoachingResponse(
        user_role_id=user_role_id,
        session_date=coaching.session_date,
        week_number=coaching.week_number,
        weekly_focus=coaching.weekly_focus or [],
        priority_topics=priority_topics,
        this_week_goals=this_week_goals,
        next_week_preview=coaching.next_week_preview or [],
        last_week_progress=coaching.last_week_progress or "Great start!",
        strengths_identified=coaching.strengths_identified or [],
        gaps_identified=coaching.gaps_identified or [],
        study_plan=coaching.study_plan or "Focus on consistent daily practice.",
        resource_recommendations=resource_recs,
        practice_recommendations=coaching.practice_recommendations or [],
        encouragement_message=coaching.encouragement_message or "Keep up the great work!",
        milestone_celebration=coaching.milestone_celebration
    )


@router.get("/velocity", response_model=LearningVelocityResponse)
async def get_learning_velocity(
    user_role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get learning velocity and engagement metrics"""
    
    # Verify ownership
    user_role = db.query(UserRole).filter(
        UserRole.id == user_role_id,
        UserRole.user_id == current_user.id
    ).first()
    
    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    # Get or generate velocity
    velocity = db.query(LearningVelocity).filter(
        LearningVelocity.user_role_id == user_role_id
    ).first()
    
    if not velocity:
        velocity = generate_learning_velocity(db, user_role_id)
    
    return LearningVelocityResponse(
        user_role_id=user_role_id,
        topics_per_week=velocity.topics_per_week,
        concepts_mastered_per_day=velocity.concepts_mastered_per_day,
        average_retention_rate=velocity.average_retention_rate,
        learning_patterns=LearningPattern(
            peak_learning_hours=velocity.peak_learning_hours or ['9-11 AM'],
            best_learning_days=velocity.best_learning_days or ['Monday', 'Wednesday'],
            preferred_learning_mode=velocity.preferred_learning_mode or 'practice'
        ),
        daily_streak=velocity.daily_streak,
        longest_streak=velocity.longest_streak,
        total_learning_hours=velocity.total_learning_hours,
        velocity_trend=velocity.velocity_trend,
        velocity_score=velocity.velocity_score,
        calculated_at=velocity.calculated_at,
        last_updated=velocity.last_updated
    )


@router.get("/dashboard", response_model=CareerIntelligenceDashboard)
async def get_intelligence_dashboard(
    user_role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get complete career intelligence dashboard"""
    
    # Get all components
    dna = await get_career_dna(user_role_id, db, current_user)
    skills = await get_skill_graph(user_role_id, db, current_user)
    forecast = await get_career_forecast(user_role_id, db, current_user)
    coaching = await get_ai_coaching(user_role_id, db, current_user)
    velocity = await get_learning_velocity(user_role_id, db, current_user)
    
    # Calculate overall readiness
    overall_readiness = (
        forecast.internship_readiness * 0.3 +
        forecast.placement_readiness * 0.4 +
        forecast.project_readiness * 0.3
    )
    
    # Determine next milestone
    if forecast.placement_readiness < 0.5:
        next_milestone = "Internship Ready"
        days_to_milestone = forecast.estimated_days_to_internship or 60
    elif forecast.placement_readiness < 0.8:
        next_milestone = "Placement Ready"
        days_to_milestone = forecast.estimated_days_to_placement or 90
    else:
        next_milestone = "Industry Expert"
        days_to_milestone = 30
    
    return CareerIntelligenceDashboard(
        career_dna=dna,
        skill_graph=skills,
        forecast=forecast,
        coaching=coaching,
        velocity=velocity,
        overall_readiness=round(overall_readiness, 2),
        next_milestone=next_milestone,
        days_to_milestone=days_to_milestone
    )


# ==================== Helper Functions ====================

def generate_career_dna(db: Session, user_role_id: int) -> CareerDNAProfile:
    """Generate Career DNA from test performance"""
    
    # Get test attempts
    attempts = db.query(MockTestAttempt).filter(
        MockTestAttempt.user_role_id == user_role_id
    ).all()
    
    scores = [a.total_score for a in attempts]
    times = [60 for a in attempts]  # Default times
    accuracy = [a.total_score / 100 for a in attempts]
    
    # Calculate DNA
    dna_data = phase6_ai_service.calculate_career_dna(scores, times, accuracy)
    
    # Determine personality type
    overall = dna_data['overall_score']
    if overall >= 0.8:
        personality = "High Achiever"
        strengths = ["Fast learner", "Consistent performer", "Problem solver"]
        improvements = ["Keep up the momentum"]
    elif overall >= 0.6:
        personality = "Steady Climber"
        strengths = ["Good consistency", "Learning efficiently"]
        improvements = ["Focus on speed", "Practice more"]
    else:
        personality = "Emerging Talent"
        strengths = ["Willingness to learn"]
        improvements = ["Build logical thinking", "Practice regularly", "Improve speed"]
    
    profile = CareerDNAProfile(
        user_role_id=user_role_id,
        logical_ability=dna_data['logical_ability'],
        problem_solving=dna_data['problem_solving'],
        speed=dna_data['speed'],
        consistency=dna_data['consistency'],
        learning_efficiency=dna_data['learning_efficiency'],
        overall_score=dna_data['overall_score'],
        personality_type=personality,
        strengths=strengths,
        improvement_areas=improvements
    )
    
    db.add(profile)
    db.commit()
    db.refresh(profile)
    
    return profile


def generate_skill_graph(db: Session, user_role_id: int) -> List[SkillGraph]:
    """Generate skill graph from completed topics"""
    
    # Get completed topics
    daily_plans = db.query(DailyPlan).filter(
        DailyPlan.user_role_id == user_role_id
    ).all()
    
    completed_topics = {}
    for plan in daily_plans:
        progress = db.query(TopicProgress).filter(
            TopicProgress.daily_plan_id == plan.id,
            TopicProgress.is_completed == True
        ).first()
        
        if progress:
            topic_name = str(plan.topic)[:30]  # Simplified
            completed_topics[topic_name] = completed_topics.get(topic_name, 0) + 1
    
    skills = []
    for topic, count in completed_topics.items():
        mastery = min(count * 0.2, 1.0)  # Each completion adds 20% mastery
        
        skill = SkillGraph(
            user_role_id=user_role_id,
            skill_name=topic,
            skill_category='technical',
            mastery_level=mastery,
            node_weight=0.5,
            connections=[],
            practice_count=count,
            last_practiced=datetime.utcnow(),
            trend='improving' if mastery < 0.8 else 'stable'
        )
        skills.append(skill)
        db.add(skill)
    
    db.commit()
    return skills


def generate_career_forecast(db: Session, user_role_id: int, role_name: str) -> CareerForecast:
    """Generate career forecast"""
    
    # Get DNA and skills
    dna = db.query(CareerDNAProfile).filter(
        CareerDNAProfile.user_role_id == user_role_id
    ).first()
    
    skills = db.query(SkillGraph).filter(
        SkillGraph.user_role_id == user_role_id
    ).all()
    
    dna_score = dna.overall_score if dna else 0.5
    skills_data = [{'mastery_level': s.mastery_level} for s in skills]
    
    # Generate forecast
    forecast_data = phase6_ai_service.generate_career_forecast(
        dna_score, skills_data, role_name
    )
    
    forecast = CareerForecast(
        user_role_id=user_role_id,
        internship_readiness=forecast_data['internship_readiness'],
        placement_readiness=forecast_data['placement_readiness'],
        project_readiness=forecast_data['project_readiness'],
        estimated_days_to_internship=forecast_data['estimated_days_to_internship'],
        estimated_days_to_placement=forecast_data['estimated_days_to_placement'],
        best_fit_roles=[
            {'role': role_name, 'match': 0.85, 'required_skills': [], 'missing_skills': [], 'days': 30}
        ],
        predicted_salary_range="6-10 LPA",
        success_probability=forecast_data['success_probability'],
        forecast_summary=forecast_data['forecast_summary'],
        recommended_actions=forecast_data['recommended_actions'],
        valid_until=datetime.utcnow() + timedelta(days=7)
    )
    
    db.add(forecast)
    db.commit()
    db.refresh(forecast)
    
    return forecast


def generate_coaching_session(db: Session, user_role_id: int) -> AICoachingSession:
    """Generate weekly coaching session"""
    
    # Get performance metrics
    metrics = db.query(UserPerformanceMetrics).filter(
        UserPerformanceMetrics.user_role_id == user_role_id
    ).first()
    
    weak_topics = []
    if metrics and metrics.weak_areas:
        weak_topics = [area['topic'] for area in metrics.weak_areas[:3]]
    
    # Calculate week number
    user_role = db.query(UserRole).filter(UserRole.id == user_role_id).first()
    weeks_since_start = ((datetime.utcnow() - user_role.created_at).days // 7) + 1
    
    coaching = AICoachingSession(
        user_role_id=user_role_id,
        week_number=weeks_since_start,
        weekly_focus=weak_topics or ['Core Concepts', 'Practice Problems'],
        priority_topics=[
            {'topic': topic, 'reason': 'Needs improvement'}
            for topic in weak_topics[:2]
        ],
        this_week_goals=[
            {'goal': 'Complete 10 practice problems', 'priority': 'high', 'hours': 5},
            {'goal': 'Review weak topics', 'priority': 'high', 'hours': 3},
            {'goal': 'Take mock test', 'priority': 'medium', 'hours': 2}
        ],
        next_week_preview=['Advanced concepts', 'Project work'],
        last_week_progress="You're making steady progress!",
        strengths_identified=['Consistency', 'Determination'],
        gaps_identified=weak_topics,
        study_plan="Focus on weak areas, practice daily, take tests weekly.",
        resource_recommendations=[
            {'type': 'practice', 'title': 'LeetCode Problems', 'link': 'https://leetcode.com', 'duration': 60}
        ],
        practice_recommendations=['Solve 2-3 problems daily', 'Review solutions'],
        encouragement_message="You're on the right track! Keep pushing forward.",
        milestone_celebration=None
    )
    
    db.add(coaching)
    db.commit()
    db.refresh(coaching)
    
    return coaching


def generate_learning_velocity(db: Session, user_role_id: int) -> LearningVelocity:
    """Generate learning velocity metrics"""
    
    # Count completed topics
    completed_count = db.query(func.count(TopicProgress.id)).join(DailyPlan).filter(
        DailyPlan.user_role_id == user_role_id,
        TopicProgress.is_completed == True
    ).scalar()
    
    # Calculate weeks since start
    user_role = db.query(UserRole).filter(UserRole.id == user_role_id).first()
    weeks = max(((datetime.utcnow() - user_role.created_at).days / 7), 1)
    
    topics_per_week = completed_count / weeks
    concepts_per_day = completed_count / max((datetime.utcnow() - user_role.created_at).days, 1)
    
    velocity = LearningVelocity(
        user_role_id=user_role_id,
        topics_per_week=round(topics_per_week, 2),
        concepts_mastered_per_day=round(concepts_per_day, 2),
        average_retention_rate=0.75,
        peak_learning_hours=['9-11 AM', '3-5 PM'],
        best_learning_days=['Monday', 'Wednesday', 'Friday'],
        preferred_learning_mode='practice',
        daily_streak=3,
        longest_streak=7,
        total_learning_hours=round(completed_count * 2.5, 1),
        velocity_trend='accelerating' if topics_per_week > 5 else 'stable',
        velocity_score=min(topics_per_week / 10, 1.0)
    )
    
    db.add(velocity)
    db.commit()
    db.refresh(velocity)
    
    return velocity
