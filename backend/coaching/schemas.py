from datetime import datetime
from typing import List

from pydantic import BaseModel


class PerCheckNote(BaseModel) :
    check: str
    result: str
    note: str


class CoachingReportSchema(BaseModel) :
    """Structured-output target passed to with_structured_output."""

    summary: str
    strengths: List[str]
    areas_to_improve: List[str]
    per_check_notes: List[PerCheckNote]


class CoachingReportResponse(CoachingReportSchema) :
    session_id: int
    overall_score: float
    generated_at: datetime
    cached: bool
