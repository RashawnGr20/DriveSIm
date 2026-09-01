from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class SessionCreate(BaseModel) :
    scenario: str
    scenario_type: Optional[str] = None
    expected_sequence: Optional[List[str]] = None


class SessionCompleteRequest(BaseModel) :
    score: float
    step_results: List[Dict[str, Any]]


class PoseStat(BaseModel) :
    count: int
    avg_duration: Optional[float] = None
    total_duration: Optional[float] = None


class SessionSummaryResponse(BaseModel) :
    session_id: int
    scenario: str
    total_events: int
    avg_duration: Optional[float] = None
    pose_breakdown: Dict[str, PoseStat]
