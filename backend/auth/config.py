import os 
import secrets

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM =    "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

