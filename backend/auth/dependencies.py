from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from .config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from backend.database.connection import get_db
from sqlalchemy.orm import Session
from backend.database.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

_credentials_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) :

    try :
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError :
        raise _credentials_exc

    user_id = payload.get("user_id")

    if user_id is None :
        raise _credentials_exc

    user = db.query(User).filter(User.id == user_id).first()

    if user is None :
        raise _credentials_exc

    return user
