from auth_client import AuthClient

auth = AuthClient()

print("Testing signup...")
signup = auth.signup("test@test.com", "password123")
print("Signup:", signup)

print("Testing login...")
login = auth.login("test@test.com", "password123")
print("Login:", login)

print("Token:", auth.token)