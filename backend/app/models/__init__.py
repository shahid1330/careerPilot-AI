# Models package
from app.models.user import User, UserRole
from app.models.roadmap import Roadmap, DailyPlan, TopicProgress
from app.models.test import MockTest, TestResult
from app.models.interview import InterviewSession, InterviewFeedback

# Phase 6A: Smart Weekly Mock Test & Evaluation System
from app.models.mock_test_v2 import (
    MockTestV2,
    MockTestQuestion,
    MockTestAttempt,
    MockTestSectionScore,
    CodingSubmission,
    UserPerformanceMetrics,
    DailyQuote
)

# Phase 6B: Career Intelligence Engine
from app.models.career_intelligence import (
    CareerDNAProfile,
    SkillGraph,
    CareerForecast,
    AICoachingSession,
    LearningVelocity
)

__all__ = [
    "User",
    "UserRole",
    "Roadmap",
    "DailyPlan",
    "TopicProgress",
    "MockTest",
    "TestResult",
    "InterviewSession",
    "InterviewFeedback",
    # Phase 6A
    "MockTestV2",
    "MockTestQuestion",
    "MockTestAttempt",
    "MockTestSectionScore",
    "CodingSubmission",
    "UserPerformanceMetrics",
    "DailyQuote",
    # Phase 6B
    "CareerDNAProfile",
    "SkillGraph",
    "CareerForecast",
    "AICoachingSession",
    "LearningVelocity",
]
