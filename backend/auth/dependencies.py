from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from jose import jwt 
from .config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from backend.database.connection import get_db
from sqlalchemy.orm import Session
from backend.database.models import User 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) :


    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    user_id = payload.get("user_id")

    user = db.query(User).filter(User.id == user_id).first()

    return user 




