from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from auth.dependencies import get_current_user
from .schemas import GazeBatchCreate
from backend.database.models import GazeEvent
from backend.database.models import Session as SessionModel
from fastapi import HTTPException
from sqlalchemy import func 

router = APIRouter(prefix="/gaze", tags=["gaze"])

@router.post("/batch")
def log_gaze_events(data: GazeBatchCreate, current_user= Depends(get_current_user), db: Session = Depends(get_db)) :

    
    session = db.query(SessionModel).filter(SessionModel.id == data.session_id).first()
    
    if not session : 
        raise HTTPException (
            status_code=404,
            detail="Session not found"
        )

    if session.user_id != current_user.id :
        raise HTTPException (
            status_code=403,
            detail="You do not have access to this session"
        )
    
    events = []

    for event in data.events:
       events.append({
        "session_id": event.session_id,
        "pose": event.pose,
        "yaw": event.yaw,
        "pitch": event.pitch,
        "duration": event.duration
    })
        

    db.bulk_insert_mappings(GazeEvent, events )
    db.commit()

    
    return {
        "status": "event recorded",
        "count": len(events)
    }

