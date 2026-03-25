"""
Phase 6A: Smart Weekly Mock Test & Evaluation System
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# ==================== MCQ Schemas ====================

class MCQOption(BaseModel):
    """Single MCQ option"""
    option_letter: str = Field(..., pattern="^[A-D]$")
    option_text: str


class MCQQuestion(BaseModel):
    """MCQ Question structure"""
    question_id: Optional[int] = None
    question_text: str
    topic: str
    difficulty: str = Field(..., pattern="^(easy|medium|hard)$")
    options: List[MCQOption]
    correct_answer: str = Field(..., pattern="^[A-D]$")
    points: int = Field(default=1, ge=1)


class MCQAnswer(BaseModel):
    """User's answer to an MCQ"""
    question_id: int
    selected_answer: str = Field(..., pattern="^[A-D]$")


# ==================== Coding Schemas ====================

class TestCase(BaseModel):
    """Single test case for coding question"""
    input: str
    output: str  # Changed from expected_output to output for consistency
    explanation: Optional[str] = None  # For visible test cases


class CodingQuestion(BaseModel):
    """Coding Question structure"""
    question_id: Optional[int] = None
    question_text: str
    topic: str
    difficulty: str = Field(..., pattern="^(easy|medium|hard)$")
    visible_test_cases: List[TestCase] = []  # Show to user
    test_cases: List[TestCase]  # All test cases (for backend)
    starter_code: Optional[str] = None
    points: int = Field(default=10, ge=1)
    language: Optional[str] = 'python'  # Programming language for this question


class CodingSubmissionRequest(BaseModel):
    """User's code submission"""
    question_id: int
    code: str
    language: str = Field(default="python")


class CodingSubmissionResult(BaseModel):
    """Result of code execution"""
    test_cases_passed: int
    total_test_cases: int
    execution_time_ms: Optional[int] = None
    is_correct: bool
    score_obtained: float
    feedback: Optional[str] = None


# ==================== Mock Test Schemas ====================

class MockTestGenerateRequest(BaseModel):
    """Request to generate a new mock test"""
    user_role_id: int
    mcq_count: int = Field(..., ge=10, le=20, description="Number of MCQs (10, 15, or 20)")
    coding_count: int = Field(..., ge=2, le=4, description="Number of coding questions (2-4)")
    test_name: Optional[str] = "Weekly Mock Test"
    test_type: str = Field(default="weekly")
    completed_day_numbers: Optional[List[int]] = Field(default=[], description="Day numbers completed from daily plan")


class MockTestResponse(BaseModel):
    """Generated mock test with questions"""
    test_id: int
    test_name: str
    test_date: datetime
    mcq_count: int
    coding_count: int
    time_limit_minutes: int
    topics_used: List[str]
    mcq_questions: List[MCQQuestion]
    coding_questions: List[CodingQuestion]
    status: str
    
    class Config:
        from_attributes = True


class MockTestSubmitRequest(BaseModel):
    """Submit complete mock test"""
    test_id: int
    user_role_id: int
    mcq_answers: List[MCQAnswer]
    coding_submissions: List[CodingSubmissionRequest]
    time_taken_minutes: int
    violations_count: Optional[int] = 0
    violations_log: Optional[List[Dict[str, str]]] = []


class SectionScore(BaseModel):
    """Score breakdown for a section"""
    section_type: str
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    unanswered: int
    score_obtained: float
    max_score: float
    percentage: float


class MockTestResult(BaseModel):
    """Complete test result with AI feedback"""
    attempt_id: int
    test_id: int
    mcq_score: float
    coding_score: float
    total_score: float
    weak_topics: List[str]
    strong_topics: List[str]
    ai_feedback: str
    improvement_plan: str
    section_scores: List[SectionScore]
    submitted_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Performance Tracking Schemas ====================

class ScoreTrend(BaseModel):
    """Single score data point"""
    date: str
    score: float
    test_name: str


class TopicAnalysis(BaseModel):
    """Topic-wise performance"""
    topic: str
    accuracy: float
    questions_attempted: int
    questions_correct: int


class PerformanceSummary(BaseModel):
    """User's overall performance analytics"""
    user_role_id: int
    total_tests_taken: int
    average_score: float
    best_score: float
    worst_score: float
    score_trend: List[ScoreTrend]
    accuracy_improvement: float
    strong_areas: List[TopicAnalysis]
    weak_areas: List[TopicAnalysis]
    last_updated: datetime
    
    class Config:
        from_attributes = True


class TestHistoryItem(BaseModel):
    """Single test in history"""
    test_id: int
    test_name: str
    test_date: datetime
    total_score: float
    mcq_score: float
    coding_score: float
    status: str
    time_taken_minutes: Optional[int] = None


class TestHistory(BaseModel):
    """List of all user's test attempts"""
    tests: List[TestHistoryItem]
    total_count: int


# ==================== Daily Quote Schemas ====================

class DailyQuoteResponse(BaseModel):
    """Daily motivational quote"""
    quote_text: str
    author: str
    category: str
    
    class Config:
        from_attributes = True
