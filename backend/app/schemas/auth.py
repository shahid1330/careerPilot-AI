"""
Authentication Schemas
Pydantic models for authentication-related requests and responses
"""

from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data"""
    username: Optional[str] = None


class LoginResponse(BaseModel):
    """Schema for login response"""
    access_token: str
    token_type: str = "bearer"
    user: dict


class MessageResponse(BaseModel):
    """Schema for generic message response"""
    message: str
    detail: Optional[str] = None
