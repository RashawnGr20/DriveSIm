from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import User 
from .schemas import SignupRequest
from .security import hash_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)) :
    

    hashed = hash_password(data.password)

    new_user = User (
        email=data.email,
        password_hash=hashed
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created"}
    