"""
Phase 6A: Mock Tests API Routes
Smart Weekly Mock Test & Evaluation System
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime, timedelta
import json

from app.core.database import get_db
from app.utils.jwt import get_current_user
from app.models.user import User, UserRole
from app.models.roadmap import DailyPlan, TopicProgress
from app.models.mock_test_v2 import (
    MockTestV2, MockTestQuestion, MockTestAttempt,
    MockTestSectionScore, CodingSubmission, UserPerformanceMetrics, DailyQuote
)
from app.schemas.mock_test_schemas import (
    MockTestGenerateRequest, MockTestResponse, MockTestSubmitRequest,
    MockTestResult, TestHistory, PerformanceSummary, DailyQuoteResponse,
    MCQQuestion, CodingQuestion, SectionScore, ScoreTrend, TopicAnalysis
)
from app.services.phase6_ai_service import phase6_ai_service
from app.utils.test_case_generator import enhance_test_cases

router = APIRouter(prefix="/mock-tests", tags=["Mock Tests"])


@router.post("/generate", response_model=MockTestResponse, status_code=status.HTTP_201_CREATED)
async def generate_mock_test(
    request: MockTestGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate personalized mock test based on completed topics
    STRICT RULE: Only uses topics user has completed/ticked from daily plans
    """
    
    # Verify user role exists
    user_role = db.query(UserRole).filter(
        UserRole.id == request.user_role_id,
        UserRole.user_id == current_user.id
    ).first()
    
    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User role not found"
        )
    
    # Get daily plans for this user role
    daily_plans = db.query(DailyPlan).filter(
        DailyPlan.user_role_id == request.user_role_id
    ).order_by(DailyPlan.day_number).all()
    
    if not daily_plans:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No daily plans found. Please generate a daily plan first."
        )
    
    # Get completed day numbers from request
    completed_day_numbers = request.completed_day_numbers or []
    
    if not completed_day_numbers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No completed topics found. Please complete at least one day from your daily plan before generating a test."
        )
    
    # Extract topics from completed days only
    completed_topics = []
    for plan in daily_plans:
        if plan.day_number in completed_day_numbers:
            # Extract topic name from plan.topic
            topic_text = plan.topic
            # Try to parse JSON if it's JSON format
            try:
                topic_data = json.loads(topic_text)
                if isinstance(topic_data, dict) and 'topic' in topic_data:
                    completed_topics.append(topic_data['topic'])
                elif isinstance(topic_data, dict) and 'name' in topic_data:
                    completed_topics.append(topic_data['name'])
                else:
                    completed_topics.append(str(topic_text)[:100])
            except:
                # Not JSON, use as is
                completed_topics.append(str(topic_text)[:100])
    
    if not completed_topics:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract topics from completed days. Please check your daily plan."
        )
    
    # Log for debugging
    print(f"\n{'='*60}")
    print(f"🎯 GENERATING MOCK TEST FOR USER ROLE: {user_role.role_name}")
    print(f"📚 Completed Day Numbers: {completed_day_numbers}")
    print(f"✅ Topics to test ({len(completed_topics)} total):")
    for idx, topic in enumerate(completed_topics, 1):
        print(f"   {idx}. {topic}")
    print(f"{'='*60}\n")
    
    # Get previous questions to avoid repetition - check last 10 tests
    previous_tests = db.query(MockTestV2).filter(
        MockTestV2.user_role_id == request.user_role_id
    ).order_by(desc(MockTestV2.test_date)).limit(10).all()
    
    previous_questions = []
    for prev_test in previous_tests:
        prev_qs = db.query(MockTestQuestion).filter(
            MockTestQuestion.test_id == prev_test.id
        ).all()
        for q in prev_qs:
            # Store more context for better uniqueness checking
            q_text = q.question_text.strip()
            # Get first 150 chars or first sentence
            first_sentence = q_text.split('.')[0] if '.' in q_text else q_text[:150]
            previous_questions.append(first_sentence.strip())
    
    # Log previous questions count
    if previous_questions:
        print(f"🔍 Found {len(previous_questions)} previous questions from {len(previous_tests)} tests")
        print(f"   AI will generate NEW questions to avoid repetition")
    else:
        print(f"✨ This is your FIRST mock test - no previous questions to avoid")
    print(f"{'='*60}\n")
    
    # Get coding language for this role
    coding_language = phase6_ai_service.get_language_for_role(user_role.role_name)
    
    # Generate questions using AI based on ONLY completed topics
    questions_data = phase6_ai_service.generate_mock_test_questions(
        completed_topics=completed_topics,
        role_name=user_role.role_name,
        mcq_count=request.mcq_count,
        coding_count=request.coding_count,
        previous_questions=previous_questions
    )
    
    # Create mock test
    mock_test = MockTestV2(
        user_role_id=request.user_role_id,
        test_name=request.test_name,
        test_type=request.test_type,
        topics_used=completed_topics,
        mcq_count=request.mcq_count,
        coding_count=request.coding_count,
        status='pending',
        time_limit_minutes=60  # Default 1 hour
    )
    
    db.add(mock_test)
    db.flush()  # Get test ID
    
    # Add MCQ questions
    for mcq_data in questions_data.get('mcq_questions', []):
        question = MockTestQuestion(
            test_id=mock_test.id,
            question_type='mcq',
            question_text=mcq_data['question_text'],
            topic=mcq_data['topic'],
            difficulty=mcq_data['difficulty'],
            options=mcq_data['options'],
            correct_answer=mcq_data['correct_answer'],
            points=mcq_data.get('points', 1)
        )
        db.add(question)
    
    # Add coding questions with visible and hidden test cases
    for coding_data in questions_data.get('coding_questions', []):
        # Handle both old and new format
        visible_tests = coding_data.get('visible_test_cases', [])
        hidden_tests = coding_data.get('hidden_test_cases', [])
        
        # Fallback: if no visible/hidden split, use test_cases
        if not visible_tests and not hidden_tests:
            all_test_cases = coding_data.get('test_cases', [])
            # Split into visible (first 3) and hidden (rest)
            visible_tests = all_test_cases[:3]
            hidden_tests = all_test_cases[3:] if len(all_test_cases) > 3 else []
        
        # Combine base test cases
        base_test_cases = visible_tests + hidden_tests
        visible_count = len(visible_tests)
        
        # 🚀 ENHANCE: Generate 50-100 comprehensive test cases
        if base_test_cases and len(base_test_cases) >= 2:
            # Generate comprehensive test cases based on difficulty
            difficulty = coding_data.get('difficulty', 'medium')
            target_count = 100 if difficulty == 'hard' else 75 if difficulty == 'medium' else 50
            
            try:
                all_test_cases = enhance_test_cases(base_test_cases, target_count=target_count)
                print(f"  → Enhanced coding question: {len(all_test_cases)} total test cases (difficulty: {difficulty})")
            except Exception as e:
                print(f"  ⚠ Test case generation failed: {e}, using base cases")
                all_test_cases = base_test_cases
        else:
            # Fallback if no base cases
            all_test_cases = [
                {"input": "test_input", "output": "expected_output"},
                {"input": "test_input2", "output": "expected_output2"}
            ]
            visible_count = 2
        
        # Store visible_count in the first test case metadata
        if all_test_cases and len(all_test_cases) > 0:
            all_test_cases[0]['_visible_count'] = visible_count
        
        question = MockTestQuestion(
            test_id=mock_test.id,
            question_type='coding',
            question_text=coding_data['question_text'],
            topic=coding_data['topic'],
            difficulty=coding_data['difficulty'],
            test_cases=all_test_cases,
            starter_code=coding_data.get('starter_code', f'# Write your {coding_language} code here'),
            language=coding_language,
            points=coding_data.get('points', 10)
        )
        db.add(question)
    
    # Store coding language in test metadata
    mock_test.topics_used = completed_topics
    if not isinstance(mock_test.topics_used, list):
        mock_test.topics_used = completed_topics
    
    db.commit()
    db.refresh(mock_test)
    
    # Prepare response
    mcq_questions_response = []
    coding_questions_response = []
    
    questions = db.query(MockTestQuestion).filter(
        MockTestQuestion.test_id == mock_test.id
    ).all()
    
    for q in questions:
        if q.question_type == 'mcq':
            mcq_questions_response.append(MCQQuestion(
                question_id=q.id,
                question_text=q.question_text,
                topic=q.topic,
                difficulty=q.difficulty,
                options=q.options,
                correct_answer=q.correct_answer,
                points=q.points
            ))
        else:
            # Get visible test cases count from question_data
            visible_count = 3  # Default
            if q.question_data and 'visible_count' in q.question_data:
                visible_count = q.question_data['visible_count']
            
            all_test_cases = q.test_cases or []
            visible_tests = all_test_cases[:visible_count]
            
            coding_questions_response.append(CodingQuestion(
                question_id=q.id,
                question_text=q.question_text,
                topic=q.topic,
                difficulty=q.difficulty,
                visible_test_cases=visible_tests,
                test_cases=all_test_cases,
                starter_code=q.starter_code,
                points=q.points,
                language=q.language or 'python'
            ))
    
    return MockTestResponse(
        test_id=mock_test.id,
        test_name=mock_test.test_name,
        test_date=mock_test.test_date,
        mcq_count=mock_test.mcq_count,
        coding_count=mock_test.coding_count,
        time_limit_minutes=mock_test.time_limit_minutes,
        topics_used=mock_test.topics_used,
        mcq_questions=mcq_questions_response,
        coding_questions=coding_questions_response,
        status=mock_test.status
    )


@router.get("/{test_id}", response_model=MockTestResponse)
async def get_mock_test(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get mock test details with questions"""
    
    mock_test = db.query(MockTestV2).filter(MockTestV2.id == test_id).first()
    
    if not mock_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mock test not found"
        )
    
    # Verify ownership
    user_role = db.query(UserRole).filter(
        UserRole.id == mock_test.user_role_id,
        UserRole.user_id == current_user.id
    ).first()
    
    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this test"
        )
    
    # Get questions
    questions = db.query(MockTestQuestion).filter(
        MockTestQuestion.test_id == test_id
    ).all()
    
    mcq_questions = []
    coding_questions = []
    
    for q in questions:
        if q.question_type == 'mcq':
            mcq_questions.append(MCQQuestion(
                question_id=q.id,
                question_text=q.question_text,
                topic=q.topic,
                difficulty=q.difficulty,
                options=q.options,
                correct_answer=q.correct_answer,
                points=q.points
            ))
        else:
            # Get visible test cases count from question_data
            visible_count = 3  # Default
            if q.question_data and 'visible_count' in q.question_data:
                visible_count = q.question_data['visible_count']
            
            all_test_cases = q.test_cases or []
            visible_tests = all_test_cases[:visible_count]
            
            coding_questions.append(CodingQuestion(
                question_id=q.id,
                question_text=q.question_text,
                topic=q.topic,
                difficulty=q.difficulty,
                visible_test_cases=visible_tests,
                test_cases=all_test_cases,
                starter_code=q.starter_code,
                points=q.points,
                language=q.language or 'python'
            ))
    
    return MockTestResponse(
        test_id=mock_test.id,
        test_name=mock_test.test_name,
        test_date=mock_test.test_date,
        mcq_count=mock_test.mcq_count,
        coding_count=mock_test.coding_count,
        time_limit_minutes=mock_test.time_limit_minutes,
        topics_used=mock_test.topics_used,
        mcq_questions=mcq_questions,
        coding_questions=coding_questions,
        status=mock_test.status
    )


@router.post("/{test_id}/submit", response_model=MockTestResult)
async def submit_mock_test(
    test_id: int,
    submission: MockTestSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit mock test and get AI-powered results"""
    
    mock_test = db.query(MockTestV2).filter(MockTestV2.id == test_id).first()
    
    if not mock_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mock test not found"
        )
    
    # Get all questions
    questions = db.query(MockTestQuestion).filter(
        MockTestQuestion.test_id == test_id
    ).all()
    
    mcq_questions = [q for q in questions if q.question_type == 'mcq']
    coding_questions = [q for q in questions if q.question_type == 'coding']
    
    # Evaluate MCQs
    mcq_correct = 0
    mcq_incorrect = 0
    mcq_total_points = 0
    mcq_earned_points = 0
    topic_performance = {}  # Track performance per topic
    
    for answer in submission.mcq_answers:
        question = next((q for q in mcq_questions if q.id == answer.question_id), None)
        if question:
            mcq_total_points += question.points
            is_correct = answer.selected_answer == question.correct_answer
            
            if is_correct:
                mcq_correct += 1
                mcq_earned_points += question.points
                topic_performance[question.topic] = topic_performance.get(question.topic, {'correct': 0, 'total': 0})
                topic_performance[question.topic]['correct'] += 1
                topic_performance[question.topic]['total'] += 1
            else:
                mcq_incorrect += 1
                topic_performance[question.topic] = topic_performance.get(question.topic, {'correct': 0, 'total': 0})
                topic_performance[question.topic]['total'] += 1
    
    mcq_score = (mcq_earned_points / mcq_total_points * 100) if mcq_total_points > 0 else 0
    
    # Evaluate coding submissions (simplified - in production, execute code)
    coding_correct = 0
    coding_total_points = 0
    coding_earned_points = 0
    
    for code_sub in submission.coding_submissions:
        question = next((q for q in coding_questions if q.id == code_sub.question_id), None)
        if question:
            coding_total_points += question.points
            
            # Simplified evaluation: 70% score if code is not empty
            # In production, execute against test cases
            test_cases_passed = len(question.test_cases) if code_sub.code.strip() else 0
            total_test_cases = len(question.test_cases)
            
            is_correct = test_cases_passed == total_test_cases
            score = (test_cases_passed / total_test_cases) * question.points if total_test_cases > 0 else 0
            
            if is_correct:
                coding_correct += 1
            
            coding_earned_points += score
            
            # Save coding submission
            coding_submission_record = CodingSubmission(
                question_id=question.id,
                code_submitted=code_sub.code,
                language=code_sub.language,
                test_cases_passed=test_cases_passed,
                total_test_cases=total_test_cases,
                is_correct=is_correct,
                score_obtained=score
            )
            db.add(coding_submission_record)
            
            # Track topic performance
            topic_performance[question.topic] = topic_performance.get(question.topic, {'correct': 0, 'total': 0})
            if is_correct:
                topic_performance[question.topic]['correct'] += 1
            topic_performance[question.topic]['total'] += 1
    
    coding_score = (coding_earned_points / coding_total_points * 100) if coding_total_points > 0 else 0
    
    # Calculate total score
    total_score = (mcq_score + coding_score) / 2
    
    # Identify weak and strong topics
    weak_topics = []
    strong_topics = []
    
    for topic, perf in topic_performance.items():
        accuracy = perf['correct'] / perf['total'] if perf['total'] > 0 else 0
        if accuracy < 0.6:
            weak_topics.append(topic)
        elif accuracy >= 0.8:
            strong_topics.append(topic)
    
    # Generate AI feedback
    feedback_data = phase6_ai_service.generate_test_feedback(
        mcq_score=mcq_score,
        coding_score=coding_score,
        weak_topics=weak_topics,
        strong_topics=strong_topics,
        role_name=mock_test.user_role.role_name
    )
    
    # Create attempt record
    attempt = MockTestAttempt(
        test_id=test_id,
        user_role_id=submission.user_role_id,
        attempt_number=1,
        submitted_at=datetime.utcnow(),
        mcq_score=mcq_score,
        coding_score=coding_score,
        total_score=total_score,
        weak_topics=weak_topics,
        strong_topics=strong_topics,
        ai_feedback=feedback_data.get('feedback', ''),
        improvement_plan=feedback_data.get('improvement_plan', ''),
        violations_count=submission.violations_count,
        violations_log=submission.violations_log
    )
    db.add(attempt)
    db.flush()
    
    # Link coding submissions to attempt
    for code_sub_record in db.query(CodingSubmission).filter(
        CodingSubmission.question_id.in_([cs.question_id for cs in submission.coding_submissions])
    ).all():
        code_sub_record.attempt_id = attempt.id
    
    # Create section scores
    mcq_section = MockTestSectionScore(
        test_id=test_id,
        attempt_id=attempt.id,
        section_type='mcq',
        total_questions=len(mcq_questions),
        correct_answers=mcq_correct,
        incorrect_answers=mcq_incorrect,
        unanswered=len(mcq_questions) - mcq_correct - mcq_incorrect,
        score_obtained=mcq_earned_points,
        max_score=mcq_total_points,
        percentage=mcq_score
    )
    db.add(mcq_section)
    
    coding_section = MockTestSectionScore(
        test_id=test_id,
        attempt_id=attempt.id,
        section_type='coding',
        total_questions=len(coding_questions),
        correct_answers=coding_correct,
        incorrect_answers=len(coding_questions) - coding_correct,
        unanswered=0,
        score_obtained=coding_earned_points,
        max_score=coding_total_points,
        percentage=coding_score
    )
    db.add(coding_section)
    
    # Update test status
    mock_test.status = 'completed'
    mock_test.completed_at = datetime.utcnow()
    mock_test.time_taken_minutes = submission.time_taken_minutes
    
    # Update user performance metrics
    update_performance_metrics(db, submission.user_role_id, total_score, topic_performance)
    
    db.commit()
    db.refresh(attempt)
    
    return MockTestResult(
        attempt_id=attempt.id,
        test_id=test_id,
        mcq_score=mcq_score,
        coding_score=coding_score,
        total_score=total_score,
        weak_topics=weak_topics,
        strong_topics=strong_topics,
        ai_feedback=attempt.ai_feedback,
        improvement_plan=attempt.improvement_plan,
        section_scores=[
            SectionScore(
                section_type='mcq',
                total_questions=mcq_section.total_questions,
                correct_answers=mcq_section.correct_answers,
                incorrect_answers=mcq_section.incorrect_answers,
                unanswered=mcq_section.unanswered,
                score_obtained=mcq_section.score_obtained,
                max_score=mcq_section.max_score,
                percentage=mcq_section.percentage
            ),
            SectionScore(
                section_type='coding',
                total_questions=coding_section.total_questions,
                correct_answers=coding_section.correct_answers,
                incorrect_answers=coding_section.incorrect_answers,
                unanswered=coding_section.unanswered,
                score_obtained=coding_section.score_obtained,
                max_score=coding_section.max_score,
                percentage=coding_section.percentage
            )
        ],
        submitted_at=attempt.submitted_at
    )


@router.get("/history", response_model=TestHistory)
async def get_test_history(
    user_role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's test history"""
    
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
    
    # Get all tests
    tests = db.query(MockTestV2).filter(
        MockTestV2.user_role_id == user_role_id
    ).order_by(desc(MockTestV2.test_date)).all()
    
    test_items = []
    for test in tests:
        attempt = db.query(MockTestAttempt).filter(
            MockTestAttempt.test_id == test.id
        ).first()
        
        test_items.append(TestHistoryItem(
            test_id=test.id,
            test_name=test.test_name,
            test_date=test.test_date,
            total_score=attempt.total_score if attempt else 0.0,
            mcq_score=attempt.mcq_score if attempt else 0.0,
            coding_score=attempt.coding_score if attempt else 0.0,
            status=test.status,
            time_taken_minutes=test.time_taken_minutes
        ))
    
    return TestHistory(tests=test_items, total_count=len(test_items))


def update_performance_metrics(db: Session, user_role_id: int, score: float, topic_performance: dict):
    """Update user performance metrics"""
    
    metrics = db.query(UserPerformanceMetrics).filter(
        UserPerformanceMetrics.user_role_id == user_role_id
    ).first()
    
    if not metrics:
        metrics = UserPerformanceMetrics(user_role_id=user_role_id)
        db.add(metrics)
    
    # Update counts
    metrics.total_tests_taken += 1
    
    # Update scores
    if metrics.total_tests_taken == 1:
        metrics.average_score = score
        metrics.best_score = score
        metrics.worst_score = score
    else:
        metrics.average_score = ((metrics.average_score * (metrics.total_tests_taken - 1)) + score) / metrics.total_tests_taken
        metrics.best_score = max(metrics.best_score, score)
        metrics.worst_score = min(metrics.worst_score, score)
    
    # Update score trend
    score_trend = metrics.score_trend or []
    score_trend.append({
        'date': datetime.utcnow().strftime('%Y-%m-%d'),
        'score': round(score, 2)
    })
    metrics.score_trend = score_trend[-10:]  # Keep last 10
    
    # Update topic analytics
    strong_areas = []
    weak_areas = []
    
    for topic, perf in topic_performance.items():
        accuracy = perf['correct'] / perf['total'] if perf['total'] > 0 else 0
        if accuracy >= 0.8:
            strong_areas.append({'topic': topic, 'accuracy': round(accuracy, 2)})
        elif accuracy < 0.6:
            weak_areas.append({'topic': topic, 'accuracy': round(accuracy, 2)})
    
    metrics.strong_areas = strong_areas
    metrics.weak_areas = weak_areas


@router.get("/daily-quote", response_model=DailyQuoteResponse)
async def get_daily_quote(db: Session = Depends(get_db)):
    """
    Get random daily motivational quote
    Returns a different quote each day (cached by date)
    """
    import random
    from datetime import date
    
    # Get all quotes
    quotes = db.query(DailyQuote).all()
    
    if not quotes:
        # Return default quote if none in database
        return DailyQuoteResponse(
            quote_text="The only way to do great work is to love what you do.",
            author="Steve Jobs",
            category="motivation"
        )
    
    # Use current date as seed for consistent daily quote
    today = date.today()
    seed = int(today.strftime('%Y%m%d'))
    random.seed(seed)
    
    quote = random.choice(quotes)
    
    return DailyQuoteResponse(
        quote_text=quote.quote_text,
        author=quote.author,
        category=quote.category
    )

