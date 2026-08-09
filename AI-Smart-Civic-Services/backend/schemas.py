from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, EmailStr, Field

CategoryType = Literal[
    'Road Damage',
    'Street Light',
    'Garbage',
    'Water Supply',
    'Sewerage',
    'Public Safety',
    'Other',
]
PriorityType = Literal['Critical', 'High', 'Medium', 'Low']
StatusType = Literal['Submitted', 'AI Analyzed', 'Assigned', 'In Progress', 'Resolved', 'Rejected']
RoleType = Literal['citizen', 'staff', 'admin']


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[RoleType] = None


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: RoleType
    created_at: datetime

    class Config:
        orm_mode = True


class ComplaintBase(BaseModel):
    title: str = Field(..., min_length=5)
    description: str = Field(..., min_length=10)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None


class ComplaintCreate(ComplaintBase):
    pass


class AIAnalysisResponse(BaseModel):
    id: int
    category: str
    priority: str
    priority_score: float
    recommended_department: str
    urgency_reason: Optional[str]
    suggested_action: Optional[str]
    keywords: Optional[str]
    possible_duplicates: Optional[str]
    model_name: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


class ComplaintStatusHistoryResponse(BaseModel):
    id: int
    status: str
    comment: Optional[str]
    changed_by_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True


class ComplaintResponse(ComplaintBase):
    id: int
    citizen_id: int
    category: CategoryType
    priority: PriorityType
    priority_score: float
    status: StatusType
    assigned_department_id: Optional[int]
    assigned_staff_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]
    ai_analyses: List[AIAnalysisResponse] = []
    status_history: List[ComplaintStatusHistoryResponse] = []

    class Config:
        orm_mode = True


class ComplaintStatusUpdate(BaseModel):
    status: StatusType
    comment: Optional[str] = None


class ComplaintAssignment(BaseModel):
    assigned_department_id: int
    assigned_staff_id: Optional[int] = None


class DepartmentResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class NotificationResponse(BaseModel):
    id: int
    complaint_id: Optional[int]
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        orm_mode = True
