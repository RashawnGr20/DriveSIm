from uuid import uuid4

from auth_client import AuthClient

auth = AuthClient()

email = f"probe+{uuid4().hex[:8]}@example.com"
password = "password123"

print("Testing signup...", email)
signup = auth.signup(email, password)
print("Signup:", signup)

print("Testing duplicate signup...")
dup = auth.signup(email, password)
print("Duplicate signup:", dup)

print("Testing login...")
login = auth.login(email, password)
print("Login:", login)

print("Testing wrong-password login...")
bad = auth.login(email, "wrong-password")
print("Bad login:", bad)

print("Token:", auth.token)
