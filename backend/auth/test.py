from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "workdingontheweeknd"

print(pwd.hash(password))