"""Script to reset database and regenerate fresh schema"""
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import create_engine, text
from app.core.base import Base
# Import all models to register them with Base
from app.models.user import User, UserRole
from app.models.roadmap import Roadmap, DailyPlan, TopicProgress
from app.models.test import MockTest, TestResult
from app.models.interview import InterviewSession, InterviewFeedback

# Local database connection
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/careerpilot_ai"

def reset_database():
    """Drop all tables and recreate fresh schema"""
    engine = create_engine(DATABASE_URL)
    
    # Drop all tables including alembic_version
    with engine.connect() as conn:
        # First check if alembic_version exists and drop it
        conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE"))
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        conn.execute(text("GRANT ALL ON SCHEMA public TO postgres"))
        conn.execute(text("GRANT ALL ON SCHEMA public TO public"))
        conn.commit()
    
    print("✅ Dropped all tables (including alembic_version) and recreated public schema")
    print("ℹ️  Database is now empty and ready for fresh migration generation")
    
    engine.dispose()

if __name__ == "__main__":
    reset_database()
