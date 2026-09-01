from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user
from backend.database.connection import get_db
from backend.database.models import Session as SessionModel

from .schemas import CoachingReportResponse
from .service import get_or_create_coaching_report

router = APIRouter(prefix="/coaching", tags=["coaching"])


@router.get("/{session_id}/report")
def get_coaching_report(session_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)) :

    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()

    if not session :
        raise HTTPException(status_code=404, detail="Session not found")

    if session.user_id != current_user.id :
        raise HTTPException(status_code=403, detail="You do not have access to this session")

    report, cached = get_or_create_coaching_report(db, session)

    return CoachingReportResponse(
        session_id=session.id,
        overall_score=report.overall_score,
        generated_at=report.created_at,
        cached=cached,
        summary=report.summary,
        strengths=report.strengths,
        areas_to_improve=report.areas_to_improve,
        per_check_notes=report.per_check_notes,
    )
