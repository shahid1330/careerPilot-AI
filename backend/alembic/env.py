"""
Alembic Environment Configuration
Handles database migration environment setup
"""

from logging.config import fileConfig
from sqlalchemy import create_engine
from sqlalchemy import pool
from alembic import context
import sys
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.core.base import Base

# Import all models to ensure they are registered with Base.metadata
from app.models.user import User, UserRole
from app.models.roadmap import Roadmap, DailyPlan, TopicProgress
from app.models.test import MockTest, TestResult
from app.models.interview import InterviewSession, InterviewFeedback

# Phase 6A & 6B: Import new models
from app.models.mock_test_v2 import (
    MockTestV2, MockTestQuestion, MockTestAttempt,
    MockTestSectionScore, CodingSubmission, UserPerformanceMetrics, DailyQuote
)
from app.models.career_intelligence import (
    CareerDNAProfile, SkillGraph, CareerForecast,
    AICoachingSession, LearningVelocity
)

# Get Alembic config object
config = context.config

# Get DATABASE_URL from environment (production) or fall back to config
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Run migrations in 'online' mode.
    
    Create an Engine and associate a connection with the context.
    Uses DATABASE_URL constructed from env variables.
    """
    # Construct DATABASE_URL from .env variables
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "careerpilot_ai")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "postgres")
    
    database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    # Create engine directly with DATABASE_URL
    connectable = create_engine(
        database_url,
        poolclass=pool.NullPool,
        pool_pre_ping=True
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
