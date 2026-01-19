"""
AI Schemas
Pydantic models for AI-related requests and responses
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class RoadmapGenerateRequest(BaseModel):
    """Schema for roadmap generation request"""
    role_name: str = Field(..., min_length=2, max_length=200, description="Job role or career path")
    duration_days: int = Field(..., ge=1, le=365, description="Number of days for the learning plan (1-365)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "role_name": "Full Stack Developer",
                "duration_days": 90
            }
        }


class RoadmapResponse(BaseModel):
    """Schema for roadmap response"""
    id: int
    user_role_id: int
    roadmap_text: str
    generated_at: datetime
    
    class Config:
        from_attributes = True


class DailyPlanGenerateRequest(BaseModel):
    """Schema for daily plan generation request"""
    user_role_id: int = Field(..., description="User role ID to associate the plan with")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_role_id": 1
            }
        }


class DailyPlanItem(BaseModel):
    """Schema for a single daily plan item"""
    id: int
    user_role_id: int
    day_number: int
    topic: str
    estimated_hours: int
    
    class Config:
        from_attributes = True


class DailyPlanResponse(BaseModel):
    """Schema for daily plan response"""
    message: str
    total_days: int
    plans: List[DailyPlanItem]
    role_name: Optional[str] = None
    user_role_id: Optional[int] = None


class TeachTopicRequest(BaseModel):
    """Schema for topic teaching request"""
    topic: str = Field(..., min_length=2, max_length=500, description="Topic to learn about")
    context: Optional[str] = Field(None, max_length=1000, description="Optional additional context for the explanation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "topic": "REST API design principles",
                "context": "Focus on best practices and common patterns"
            }
        }


class TeachTopicResponse(BaseModel):
    """Schema for topic teaching response"""
    topic: str
    explanation: str
    examples: List[str]
    resources: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "topic": "REST API design principles",
                "explanation": "REST (Representational State Transfer) is an architectural style...",
                "examples": ["GET /users - retrieve users", "POST /users - create user"],
                "resources": [
                    "https://www.geeksforgeeks.org/rest-api",
                    "https://www.w3schools.com/rest/",
                    "YouTube: REST API Tutorial"
                ]
            }
        }
