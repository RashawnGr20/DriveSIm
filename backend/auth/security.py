from passlib.context import CryptContext

pswd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash_password(password) :
    return pswd_context.hash(password)

def verify_password(password, hashed) :
    return pswd_context.verify(password, hashed)