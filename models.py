# models.py - Pydantic models for request/response

from pydantic import BaseModel
from typing import Optional, List, Dict


class LoginRequest(BaseModel):
    """Login request model"""
    username: str
    password: str


class QueryRequest(BaseModel):
    """Query request model"""
    question: str
    context_length: Optional[int] = 2


class QueryResponse(BaseModel):
    """Query response model"""
    question: str
    answer: str
    cached: bool
    response_time: float
    user: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    query_engine_initialized: bool
    cached_queries: int


class DashboardResponse(BaseModel):
    """Dashboard metrics response"""
    status: str
    user: str
    role: str
    total_queries: int
    total_users: int
    cached_queries: int
    avg_response_time: float


class TokenResponse(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str
    role: str


class HistoryResponse(BaseModel):
    """Query history response"""
    user: str
    query_count: int
    history: List[Dict]
