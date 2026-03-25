"""
Phase 6A: Performance & Daily Quotes API
Performance analytics and daily motivational quotes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List
import random

from app.core.database import get_db
from app.utils.jwt import get_current_user
from app.models.user import User, UserRole
from app.models.mock_test_v2 import UserPerformanceMetrics, DailyQuote
from app.schemas.mock_test_schemas import PerformanceSummary, DailyQuoteResponse, ScoreTrend, TopicAnalysis

router = APIRouter(tags=["Performance & Quotes"])


@router.get("/performance/summary", response_model=PerformanceSummary)
async def get_performance_summary(
    user_role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get comprehensive performance analytics"""
    
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
    
    # Get performance metrics
    metrics = db.query(UserPerformanceMetrics).filter(
        UserPerformanceMetrics.user_role_id == user_role_id
    ).first()
    
    if not metrics:
        # Return default metrics if no tests taken yet
        return PerformanceSummary(
            user_role_id=user_role_id,
            total_tests_taken=0,
            average_score=0.0,
            best_score=0.0,
            worst_score=0.0,
            score_trend=[],
            accuracy_improvement=0.0,
            strong_areas=[],
            weak_areas=[],
            last_updated=datetime.utcnow()
        )
    
    # Parse score trend
    score_trend = []
    if metrics.score_trend:
        for item in metrics.score_trend:
            score_trend.append(ScoreTrend(
                date=item['date'],
                score=item['score'],
                test_name=f"Test {len(score_trend) + 1}"
            ))
    
    # Parse topic analytics
    strong_areas = []
    if metrics.strong_areas:
        for item in metrics.strong_areas:
            strong_areas.append(TopicAnalysis(
                topic=item['topic'],
                accuracy=item['accuracy'],
                questions_attempted=10,  # Placeholder
                questions_correct=int(item['accuracy'] * 10)
            ))
    
    weak_areas = []
    if metrics.weak_areas:
        for item in metrics.weak_areas:
            weak_areas.append(TopicAnalysis(
                topic=item['topic'],
                accuracy=item['accuracy'],
                questions_attempted=10,
                questions_correct=int(item['accuracy'] * 10)
            ))
    
    return PerformanceSummary(
        user_role_id=user_role_id,
        total_tests_taken=metrics.total_tests_taken,
        average_score=round(metrics.average_score, 2),
        best_score=round(metrics.best_score, 2),
        worst_score=round(metrics.worst_score, 2),
        score_trend=score_trend,
        accuracy_improvement=round(metrics.accuracy_improvement, 2),
        strong_areas=strong_areas,
        weak_areas=weak_areas,
        last_updated=metrics.last_updated
    )


@router.get("/daily-quote", response_model=DailyQuoteResponse)
async def get_daily_quote(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get daily motivational quote"""
    
    # Check if we have quotes in database
    quote_count = db.query(func.count(DailyQuote.id)).scalar()
    
    if quote_count == 0:
        # Seed initial quotes
        seed_quotes(db)
    
    # Get today's quote (simple random for now)
    # In production, use date-based selection for consistency
    today = datetime.utcnow().date()
    quote_id = (today.toordinal() % db.query(func.count(DailyQuote.id)).scalar()) + 1
    
    quote = db.query(DailyQuote).filter(DailyQuote.id == quote_id).first()
    
    if not quote:
        quote = db.query(DailyQuote).first()
    
    if not quote:
        # Fallback quote
        return DailyQuoteResponse(
            quote_text="The only way to do great work is to love what you do.",
            author="Steve Jobs",
            category="motivation"
        )
    
    return DailyQuoteResponse(
        quote_text=quote.quote_text,
        author=quote.author,
        category=quote.category
    )


def seed_quotes(db: Session):
    """Seed database with motivational quotes"""
    
    quotes = [
        {
            "text": "The only way to do great work is to love what you do.",
            "author": "Steve Jobs",
            "category": "motivation"
        },
        {
            "text": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
            "author": "Winston Churchill",
            "category": "success"
        },
        {
            "text": "Learning never exhausts the mind.",
            "author": "Leonardo da Vinci",
            "category": "learning"
        },
        {
            "text": "The expert in anything was once a beginner.",
            "author": "Helen Hayes",
            "category": "learning"
        },
        {
            "text": "Success is the sum of small efforts repeated day in and day out.",
            "author": "Robert Collier",
            "category": "success"
        },
        {
            "text": "The future belongs to those who believe in the beauty of their dreams.",
            "author": "Eleanor Roosevelt",
            "category": "motivation"
        },
        {
            "text": "Code is like humor. When you have to explain it, it's bad.",
            "author": "Cory House",
            "category": "motivation"
        },
        {
            "text": "First, solve the problem. Then, write the code.",
            "author": "John Johnson",
            "category": "learning"
        },
        {
            "text": "Programming isn't about what you know; it's about what you can figure out.",
            "author": "Chris Pine",
            "category": "learning"
        },
        {
            "text": "The best error message is the one that never shows up.",
            "author": "Thomas Fuchs",
            "category": "motivation"
        }
    ]
    
    for q in quotes:
        quote = DailyQuote(
            quote_text=q["text"],
            author=q["author"],
            category=q["category"]
        )
        db.add(quote)
    
    db.commit()
