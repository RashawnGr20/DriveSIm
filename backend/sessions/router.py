from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user
from backend.database.connection import get_db
from .schemas import SessionCreate
from backend.database.models import Session as SessionModel

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
    