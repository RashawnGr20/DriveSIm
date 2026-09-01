from datetime import datetime

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from backend.auth.dependencies import get_current_user
from backend.database.connection import get_db
from .schemas import SessionCreate, SessionCompleteRequest
from .service import get_pose_breakdown
from backend.database.models import Session as SessionModel
from backend.database.models import GazeEvent
from sqlalchemy import func
from fastapi import HTTPException

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/")
def log_session(data: SessionCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)) :


    session = SessionModel (
        user_id = current_user.id,
        scenario = data.scenario,
        scenario_type = data.scenario_type,
        expected_sequence = data.expected_sequence
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return {"session_id": session.id}


@router.post("/{session_id}/complete")
def complete_session(session_id: int, data: SessionCompleteRequest, current_user = Depends(get_current_user), db: Session = Depends(get_db)) :

    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()

    if not session :
        raise HTTPException(status_code=404, detail="Session not found")

    if session.user_id != current_user.id :
        raise HTTPException (
            status_code=403,
            detail="You do not have access to this session"
        )

    session.score = data.score
    session.step_results = data.step_results
    session.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(session)

    return {
        "session_id": session.id,
        "score": session.score,
        "completed_at": session.completed_at
    }


@router.get("/{session_id}/summary")
def get_session_summary(session_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)) :

    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()

    if not session :
        raise HTTPException(status_code=404, detail="Session not found")

    if session.user_id != current_user.id :
        raise HTTPException (
            status_code=403,
            detail="You do not have access to this session"
        )

    total_events = db.query(func.count(GazeEvent.id)).filter(GazeEvent.session_id == session_id).scalar()

    avg_duration = db.query(func.avg(GazeEvent.duration)).filter(GazeEvent.session_id == session_id).scalar()

    pose_breakdown = get_pose_breakdown(db, session_id)

    return {
        "session_id": session.id,
        "scenario": session.scenario,
        "total_events": total_events,
        "avg_duration": avg_duration,
        "pose_breakdown": pose_breakdown
    }

@router.get("/")
def get_sessions(current_user = Depends(get_current_user), db: Session = Depends(get_db)) :

    sessions = db.query(SessionModel).filter(SessionModel.user_id == current_user.id).all()

    return [
        {
            "session_id": s.id,
            "scenario": s.scenario,
            "score": s.score,
            "created_at": s.created_at
        }
        for s in sessions
    ]



