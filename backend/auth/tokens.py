from jose import jwt 
from .config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from datetime import datetime, timedelta


def create_access_token(data) :
    
    current_time = datetime.utcnow()

    payload =  data.copy()

    expiration = current_time + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload["exp"] = expiration

    token  = jwt.encode(payload, SECRET_KEY, ALGORITHM)

    return token 