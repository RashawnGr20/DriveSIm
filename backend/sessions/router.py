from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user
from backend.database.connection import get_db
from .schemas import SessionCreate
from backend.database.models import Session as SessionModel
from backend.database.models import GazeEvent
from sqlalchemy import func
from fastapi import HTTPException

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/")
def log_session(data: SessionCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)) :

    
    session = SessionModel (
        user_id = current_user.id,
        scenario = data.scenario
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return {"session_id": session.id}


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

    mirror_checks = db.query(func.count(GazeEvent.id)).filter(GazeEvent.session_id == session_id, GazeEvent.pose == "LEFT_MIRROR").scalar()

    return {
        "session_id": session.id,
        "scenario": session.scenario, 
        "total_events": total_events,
        "mirror_checks": mirror_checks,
        "avg_duration": avg_duration
    }

@router.get("/") 
def get_sessions(current_user = Depends(SessionModel), db: Session = Depends(get_db)) :

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
    


