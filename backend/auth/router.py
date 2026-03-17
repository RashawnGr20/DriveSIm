from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import LoginRequest
from backend.database.connection import get_db
from backend.database.models import User 
from .schemas import SignupRequest
from .security import hash_password
from .security import verify_password
from .tokens import create_access_token

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

    print("USER CREATED:", new_user.id)

    return {"message": "User created"}


    
@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)) :

    user = db.query(User).filter(User.email == data.email).first()

    if not user : 
        return {"error": "invalid credentials"}

    if not verify_password(data.password, user.password_hash) :
        return {"error": "invalid credentials"}
    
    token = create_access_token({"user_id": user.id})


    return { 
        "access_token": token, 
        "token_type": "bearer"
    }
    







    