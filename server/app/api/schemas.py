from typing import Optional, Dict, Any
from pydantic import BaseModel

class ExecuteGoalRequest(BaseModel):
    goal: str
    model: Optional[str] = "simulation"

class ApprovalActionRequest(BaseModel):
    approval_id: str
    approved: bool

class StandardResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
