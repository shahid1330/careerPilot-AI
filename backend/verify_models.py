"""
Quick verification script to test model imports and basic structure
Run this to verify all models are correctly configured
"""

import sys
sys.path.append(".")

try:
    # Test imports
    print("Testing model imports...")
    from app.models.user import User, UserRole
    from app.models.roadmap import Roadmap, DailyPlan, TopicProgress
    from app.models.test import MockTest, TestResult
    from app.models.interview import InterviewSession, InterviewFeedback
    print("✅ All models imported successfully")
    
    # Test schema imports
    print("\nTesting schema imports...")
    from app.schemas.user import UserCreate, UserResponse, UserDetailResponse
    from app.schemas.auth import Token, LoginResponse
    print("✅ All schemas imported successfully")
    
    # Test core imports
    print("\nTesting core imports...")
    from app.core.config import settings
    from app.core.database import get_db
    from app.core.base import Base
    print("✅ Core modules imported successfully")
    
    # Test utils imports
    print("\nTesting utils imports...")
    from app.utils.security import hash_password, verify_password
    from app.utils.jwt import create_access_token, verify_token
    print("✅ Utils imported successfully")
    
    # Verify User model has correct fields
    print("\n" + "="*50)
    print("VERIFYING USER MODEL FIELDS")
    print("="*50)
    user_columns = [c.name for c in User.__table__.columns]
    print(f"User table columns: {user_columns}")
    assert "password_hash" in user_columns, "❌ password_hash not found"
    assert "hashed_password" not in user_columns, "❌ hashed_password should not exist"
    assert "full_name" in user_columns, "❌ full_name not found"
    assert "updated_at" not in user_columns, "❌ updated_at should not exist"
    print("✅ User model fields are correct")
    
    # Verify UserRole model
    print("\n" + "="*50)
    print("VERIFYING USER_ROLE MODEL FIELDS")
    print("="*50)
    role_columns = [c.name for c in UserRole.__table__.columns]
    print(f"UserRole table columns: {role_columns}")
    assert "duration_days" in role_columns, "❌ duration_days not found"
    assert "granted_at" not in role_columns, "❌ granted_at should not exist"
    print("✅ UserRole model fields are correct")
    
    # Verify Roadmap model
    print("\n" + "="*50)
    print("VERIFYING ROADMAP MODEL FIELDS")
    print("="*50)
    roadmap_columns = [c.name for c in Roadmap.__table__.columns]
    print(f"Roadmap table columns: {roadmap_columns}")
    assert "user_role_id" in roadmap_columns, "❌ user_role_id not found"
    assert "roadmap_text" in roadmap_columns, "❌ roadmap_text not found"
    assert "user_id" not in roadmap_columns, "❌ user_id should not exist"
    assert "career_goal" not in roadmap_columns, "❌ career_goal should not exist"
    print("✅ Roadmap model fields are correct")
    
    # Verify DailyPlan model
    print("\n" + "="*50)
    print("VERIFYING DAILY_PLAN MODEL FIELDS")
    print("="*50)
    daily_plan_columns = [c.name for c in DailyPlan.__table__.columns]
    print(f"DailyPlan table columns: {daily_plan_columns}")
    assert "user_role_id" in daily_plan_columns, "❌ user_role_id not found"
    assert "estimated_hours" in daily_plan_columns, "❌ estimated_hours not found"
    assert "roadmap_id" not in daily_plan_columns, "❌ roadmap_id should not exist"
    print("✅ DailyPlan model fields are correct")
    
    # Verify TopicProgress model
    print("\n" + "="*50)
    print("VERIFYING TOPIC_PROGRESS MODEL FIELDS")
    print("="*50)
    topic_progress_columns = [c.name for c in TopicProgress.__table__.columns]
    print(f"TopicProgress table columns: {topic_progress_columns}")
    assert "daily_plan_id" in topic_progress_columns, "❌ daily_plan_id not found"
    assert "is_completed" in topic_progress_columns, "❌ is_completed not found"
    assert "roadmap_id" not in topic_progress_columns, "❌ roadmap_id should not exist"
    assert "topic_name" not in topic_progress_columns, "❌ topic_name should not exist"
    print("✅ TopicProgress model fields are correct")
    
    # Verify MockTest model
    print("\n" + "="*50)
    print("VERIFYING MOCK_TEST MODEL FIELDS")
    print("="*50)
    mock_test_columns = [c.name for c in MockTest.__table__.columns]
    print(f"MockTest table columns: {mock_test_columns}")
    assert "user_role_id" in mock_test_columns, "❌ user_role_id not found"
    assert "test_type" in mock_test_columns, "❌ test_type not found"
    assert "test_date" in mock_test_columns, "❌ test_date not found"
    assert "title" not in mock_test_columns, "❌ title should not exist"
    print("✅ MockTest model fields are correct")
    
    # Verify TestResult model
    print("\n" + "="*50)
    print("VERIFYING TEST_RESULT MODEL FIELDS")
    print("="*50)
    test_result_columns = [c.name for c in TestResult.__table__.columns]
    print(f"TestResult table columns: {test_result_columns}")
    assert "mock_test_id" in test_result_columns, "❌ mock_test_id not found"
    assert "score" in test_result_columns, "❌ score not found"
    assert "user_id" not in test_result_columns, "❌ user_id should not exist"
    assert "test_id" not in test_result_columns, "❌ test_id should not exist"
    print("✅ TestResult model fields are correct")
    
    # Verify InterviewSession model
    print("\n" + "="*50)
    print("VERIFYING INTERVIEW_SESSION MODEL FIELDS")
    print("="*50)
    interview_session_columns = [c.name for c in InterviewSession.__table__.columns]
    print(f"InterviewSession table columns: {interview_session_columns}")
    assert "user_role_id" in interview_session_columns, "❌ user_role_id not found"
    assert "interview_date" in interview_session_columns, "❌ interview_date not found"
    assert "user_id" not in interview_session_columns, "❌ user_id should not exist"
    print("✅ InterviewSession model fields are correct")
    
    # Verify InterviewFeedback model
    print("\n" + "="*50)
    print("VERIFYING INTERVIEW_FEEDBACK MODEL FIELDS")
    print("="*50)
    interview_feedback_columns = [c.name for c in InterviewFeedback.__table__.columns]
    print(f"InterviewFeedback table columns: {interview_feedback_columns}")
    assert "interview_session_id" in interview_feedback_columns, "❌ interview_session_id not found"
    assert "weaknesses" in interview_feedback_columns, "❌ weaknesses not found"
    assert "overall_score" in interview_feedback_columns, "❌ overall_score not found"
    assert "session_id" not in interview_feedback_columns, "❌ session_id should not exist"
    print("✅ InterviewFeedback model fields are correct")
    
    print("\n" + "="*50)
    print("🎉 ALL VERIFICATION CHECKS PASSED!")
    print("="*50)
    print("\n✅ Backend code is aligned with database schema")
    print("✅ Ready to run: uvicorn main:app --reload")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)
except AssertionError as e:
    print(f"❌ Assertion Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
