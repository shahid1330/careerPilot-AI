"""
AI Router
Handles AI-powered endpoints for roadmap generation, daily plans, and topic teaching
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User, UserRole
from app.models.roadmap import DailyPlan, Roadmap
from app.utils.jwt import get_current_user
from app.schemas.ai import (
    RoadmapGenerateRequest,
    RoadmapResponse,
    DailyPlanGenerateRequest,
    DailyPlanResponse,
    DailyPlanItem,
    TeachTopicRequest,
    TeachTopicResponse
)
from app.services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["AI & LLM"])


@router.post(
    "/generate-roadmap",
    response_model=RoadmapResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate Career Roadmap",
    description="Use AI to generate a comprehensive career roadmap with required skills and learning path"
)
async def generate_roadmap(
    request: RoadmapGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate a career roadmap using AI
    
    - **role_name**: Job role or career path (e.g., "Full Stack Developer")
    - **duration_days**: Number of days for the learning plan (1-365)
    
    The AI will generate:
    - Required skills for the role
    - Phased learning path (Fundamentals → Intermediate → Advanced)
    - Recommended projects
    
    Returns the generated roadmap stored in the database.
    """
    try:
        roadmap = await AIService.generate_roadmap(
            role_name=request.role_name,
            duration_days=request.duration_days,
            user_id=current_user.id,
            db=db
        )
        return roadmap
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate roadmap: {str(e)}"
        )


@router.post(
    "/generate-daily-plan",
    response_model=DailyPlanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate Daily Learning Plan",
    description="Use AI to generate a day-by-day learning plan for a specific role and timeframe"
)
async def generate_daily_plan(
    request: DailyPlanGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate a daily learning plan using AI
    
    - **user_role_id**: User role ID (contains role and duration info from roadmap)
    
    The AI will generate a structured day-by-day plan with:
    - Daily topics building progressively
    - Estimated hours for each day (2-6 hours)
    - Coverage from fundamentals to advanced concepts
    
    If a plan already exists for this role, it will be regenerated based on the current duration.
    """
    try:
        # Check if user owns this user_role
        user_role = db.query(UserRole).filter(
            UserRole.id == request.user_role_id,
            UserRole.user_id == current_user.id
        ).first()
        
        if not user_role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User role not found or does not belong to you"
            )
        
        daily_plans = await AIService.generate_daily_plan(
            user_role_id=request.user_role_id,
            db=db
        )
        
        # Convert to response schema
        plan_items = [
            DailyPlanItem(
                id=plan.id,
                user_role_id=plan.user_role_id,
                day_number=plan.day_number,
                topic=plan.topic,
                estimated_hours=plan.estimated_hours
            )
            for plan in daily_plans
        ]
        
        return DailyPlanResponse(
            message=f"Successfully generated {len(plan_items)}-day learning plan",
            total_days=len(plan_items),
            plans=plan_items
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate daily plan: {str(e)}"
        )


@router.post(
    "/teach-topic",
    response_model=TeachTopicResponse,
    summary="AI Topic Teaching",
    description="Get an AI-powered explanation of any topic with examples and learning resources"
)
async def teach_topic(
    request: TeachTopicRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Get an educational explanation of a topic using AI
    
    - **topic**: Any topic you want to learn about (e.g., "REST API design principles")
    - **context**: Optional additional context for better explanations
    
    The AI will provide:
    - Clear, beginner-friendly explanation
    - Practical examples with code/scenarios
    - Learning resources (GeeksforGeeks, W3Schools, YouTube, Documentation)
    
    This endpoint does NOT store results in the database - it returns the explanation directly.
    """
    try:
        teaching_data = await AIService.teach_topic(
            topic=request.topic,
            context=request.context
        )
        
        return TeachTopicResponse(
            topic=teaching_data.get("topic", request.topic),
            explanation=teaching_data.get("explanation", ""),
            examples=teaching_data.get("examples", []),
            resources=teaching_data.get("resources", [])
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate topic explanation: {str(e)}"
        )


@router.get(
    "/daily-plans",
    response_model=List[DailyPlanResponse],
    summary="Get All Daily Plans",
    description="Fetch all daily plans for the current user grouped by user_role_id"
)
async def get_daily_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all daily plans for the current user
    
    Returns all daily plans grouped by user roles (different learning paths)
    """
    try:
        # Get all user roles for this user
        user_roles = db.query(UserRole).filter(UserRole.user_id == current_user.id).all()
        
        if not user_roles:
            return []
        
        # Deduplicate roles by name - keep only the most recent one
        unique_roles = {}
        for user_role in user_roles:
            role_key = user_role.role_name.lower()
            if role_key not in unique_roles or user_role.id > unique_roles[role_key].id:
                unique_roles[role_key] = user_role
        
        # Fetch daily plans for each unique role
        all_plans = []
        for user_role in unique_roles.values():
            daily_plans = db.query(DailyPlan).filter(
                DailyPlan.user_role_id == user_role.id
            ).order_by(DailyPlan.day_number).all()
            
            if daily_plans:
                plan_items = [
                    DailyPlanItem(
                        id=plan.id,
                        user_role_id=plan.user_role_id,
                        day_number=plan.day_number,
                        topic=plan.topic,
                        estimated_hours=plan.estimated_hours
                    )
                    for plan in daily_plans
                ]
                
                all_plans.append(DailyPlanResponse(
                    message=f"Daily plan for {user_role.role_name}",
                    total_days=len(plan_items),
                    plans=plan_items,
                    role_name=user_role.role_name,
                    user_role_id=user_role.id
                ))
        
        return all_plans
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch daily plans: {str(e)}"
        )


@router.delete(
    "/daily-plans/{user_role_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Daily Plan",
    description="Delete a user role and all associated daily plans"
)
async def delete_daily_plan(
    user_role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a daily plan and associated user role
    
    This will permanently delete:
    - The user role entry
    - All daily plans for that role
    - The roadmap for that role
    """
    try:
        # Check if user owns this user_role
        user_role = db.query(UserRole).filter(
            UserRole.id == user_role_id,
            UserRole.user_id == current_user.id
        ).first()
        
        if not user_role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User role not found or does not belong to you"
            )
        
        role_name = user_role.role_name
        
        # Delete daily plans
        db.query(DailyPlan).filter(DailyPlan.user_role_id == user_role_id).delete()
        
        # Delete roadmap
        db.query(Roadmap).filter(Roadmap.user_role_id == user_role_id).delete()
        
        # Delete user role
        db.delete(user_role)
        db.commit()
        
        return {
            "message": f"Successfully deleted daily plan for {role_name}",
            "deleted_role": role_name
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete daily plan: {str(e)}"
        )


@router.delete(
    "/roadmaps/{user_role_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Roadmap",
    description="Delete a roadmap and associated user role"
)
async def delete_roadmap(
    user_role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a roadmap and associated user role
    
    This will permanently delete:
    - The roadmap
    - The user role entry
    - All daily plans for that role
    """
    try:
        # Check if user owns this user_role
        user_role = db.query(UserRole).filter(
            UserRole.id == user_role_id,
            UserRole.user_id == current_user.id
        ).first()
        
        if not user_role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User role not found or does not belong to you"
            )
        
        role_name = user_role.role_name
        
        # Delete daily plans
        db.query(DailyPlan).filter(DailyPlan.user_role_id == user_role_id).delete()
        
        # Delete roadmap
        db.query(Roadmap).filter(Roadmap.user_role_id == user_role_id).delete()
        
        # Delete user role
        db.delete(user_role)
        db.commit()
        
        return {
            "message": f"Successfully deleted roadmap for {role_name}",
            "deleted_role": role_name
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete roadmap: {str(e)}"
        )
