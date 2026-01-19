"""
AI Service
Business logic for AI-powered features
"""

import json
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from datetime import datetime

from app.ai.groq_client import groq_client
from app.ai.prompts import PromptTemplates
from app.models.roadmap import Roadmap, DailyPlan
from app.models.user import UserRole


class AIService:
    """
    Service layer for AI-powered features
    """
    
    @staticmethod
    async def generate_roadmap(role_name: str, duration_days: int, user_id: int, db: Session) -> Roadmap:
        """
        Generate a career roadmap using LLM and store in database
        Auto-creates or updates UserRole entry for the user
        
        Args:
            role_name: The job role or career path
            duration_days: Duration in days for the learning plan
            user_id: Current user ID
            db: Database session
            
        Returns:
            Created Roadmap object
            
        Raises:
            Exception: If LLM generation or database operation fails
        """
        # Check if UserRole already exists for this user and role
        user_role = db.query(UserRole).filter(
            UserRole.user_id == user_id,
            UserRole.role_name == role_name
        ).first()
        
        if user_role:
            # Update existing UserRole with new duration
            user_role.duration_days = duration_days
            # Delete old roadmap and daily plans for this role
            db.query(Roadmap).filter(Roadmap.user_role_id == user_role.id).delete()
            db.query(DailyPlan).filter(DailyPlan.user_role_id == user_role.id).delete()
        else:
            # Create new UserRole entry for this learning goal
            user_role = UserRole(
                user_id=user_id,
                role_name=role_name,
                duration_days=duration_days
            )
            db.add(user_role)
        
        db.flush()  # Get the ID without committing
        
        # Generate prompt
        prompt = PromptTemplates.roadmap_generation(role_name, duration_days)
        
        # Get LLM response
        try:
            roadmap_data = await groq_client.generate_json_completion(prompt, temperature=0.7)
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to generate roadmap: {str(e)}")
        
        # Convert to JSON string for storage
        roadmap_text = json.dumps(roadmap_data, indent=2)
        
        # Create roadmap in database
        roadmap = Roadmap(
            user_role_id=user_role.id,
            roadmap_text=roadmap_text
        )
        
        db.add(roadmap)
        db.commit()
        db.refresh(roadmap)
        
        return roadmap
    
    @staticmethod
    async def generate_daily_plan(
        user_role_id: int,
        db: Session
    ) -> List[DailyPlan]:
        """
        Generate a daily learning plan using LLM and store in database
        
        Args:
            user_role_id: User role ID to associate with (contains role_name and duration)
            db: Database session
            
        Returns:
            List of created DailyPlan objects
            
        Raises:
            Exception: If LLM generation or database operation fails
        """
        # Fetch user_role to get role_name and duration_days
        user_role = db.query(UserRole).filter(UserRole.id == user_role_id).first()
        if not user_role:
            raise ValueError(f"UserRole with id {user_role_id} not found")
        
        # Delete existing daily plans for this user_role_id to avoid duplicates
        db.query(DailyPlan).filter(DailyPlan.user_role_id == user_role_id).delete()
        db.commit()
        
        # Extract role_name and duration_days from UserRole
        role_name = user_role.role_name
        duration_days = user_role.duration_days
        
        # Validate duration
        if duration_days < 1 or duration_days > 365:
            raise ValueError("Duration must be between 1 and 365 days")
        
        # Generate prompt
        prompt = PromptTemplates.daily_plan_generation(role_name, duration_days)
        
        # Get LLM response
        try:
            plan_data = await groq_client.generate_json_completion(prompt, temperature=0.7, max_tokens=3000)
        except Exception as e:
            raise Exception(f"Failed to generate daily plan: {str(e)}")
        
        # Validate response structure
        if "daily_plan" not in plan_data:
            raise Exception("LLM response missing 'daily_plan' field")
        
        # Create daily plan entries
        daily_plans = []
        llm_daily_plan = plan_data.get("daily_plan", [])
        
        # Ensure we have exactly duration_days entries
        if len(llm_daily_plan) > duration_days:
            # Trim if LLM generated too many
            llm_daily_plan = llm_daily_plan[:duration_days]
        elif len(llm_daily_plan) < duration_days:
            # Pad if LLM generated too few
            last_day = len(llm_daily_plan)
            for day_num in range(last_day + 1, duration_days + 1):
                llm_daily_plan.append({
                    "day": day_num,
                    "topic": f"Advanced {role_name} Concepts - Day {day_num}",
                    "estimated_hours": 4
                })
        
        for day_item in llm_daily_plan:
            try:
                daily_plan = DailyPlan(
                    user_role_id=user_role_id,
                    day_number=day_item.get("day", 0),
                    topic=day_item.get("topic", ""),
                    estimated_hours=int(day_item.get("estimated_hours", 3))
                )
                daily_plans.append(daily_plan)
            except (KeyError, ValueError) as e:
                # Skip invalid entries but log them
                print(f"Skipping invalid daily plan entry: {day_item}. Error: {e}")
                continue
        
        if not daily_plans:
            raise Exception("No valid daily plans generated")
        
        # Bulk insert
        db.add_all(daily_plans)
        db.commit()
        
        # Refresh all objects
        for plan in daily_plans:
            db.refresh(plan)
        
        return daily_plans
    
    @staticmethod
    async def teach_topic(topic: str, context: str = None) -> Dict[str, Any]:
        """
        Get an educational explanation of a topic using LLM
        
        Args:
            topic: The topic to explain
            context: Optional additional context for the explanation
            
        Returns:
            Dictionary with explanation, examples, and resources
            
        Raises:
            Exception: If LLM generation fails
        """
        # Generate prompt
        prompt = PromptTemplates.teach_topic(topic, context)
        
        # Get LLM response
        try:
            teaching_data = await groq_client.generate_json_completion(prompt, temperature=0.7)
        except Exception as e:
            raise Exception(f"Failed to generate topic explanation: {str(e)}")
        
        # Validate response structure
        required_fields = ["topic", "explanation", "examples", "resources"]
        for field in required_fields:
            if field not in teaching_data:
                teaching_data[field] = [] if field in ["examples", "resources"] else ""
        
        return teaching_data
