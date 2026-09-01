from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .schemas import LoginRequest
from backend.database.connection import get_db
from backend.database.models import User
from .schemas import SignupRequest
from .schemas import TokenResponse
from .security import hash_password
from .security import verify_password
from .tokens import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=TokenResponse)
def signup(data: SignupRequest, db: Session = Depends(get_db)) :

    existing = db.query(User).filter(User.email == data.email).first()

    if existing :
        raise HTTPException(status_code=409, detail="email already registered")

    hashed = hash_password(data.password)

    new_user = User (
        email=data.email,
        password_hash=hashed
    )

    db.add(new_user)

    try :
        db.commit()
    except IntegrityError :
        db.rollback()
        raise HTTPException(status_code=409, detail="email already registered")

    db.refresh(new_user)

    print("USER CREATED:", new_user.id)

    token = create_access_token({"user_id": new_user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }



@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)) :

    user = db.query(User).filter(User.email == data.email).first()

    if not user :
        raise HTTPException(status_code=401, detail="invalid credentials")

    if not verify_password(data.password, user.password_hash) :
        raise HTTPException(status_code=401, detail="invalid credentials")

    token = create_access_token({"user_id": user.id})


    return {
        "access_token": token,
        "token_type": "bearer"
    }
