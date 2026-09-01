import requests

BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 10

UNREACHABLE_MSG = "Couldn't reach the server. Is the backend running?"


class AuthClient :

    def __init__(self):
        self.token = None


    def login(self, email, password ) :

        try :
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json={
                    "email": email,
                    "password": password
                },
                timeout=TIMEOUT,
            )
        except requests.exceptions.RequestException as e :
            print("login request failed:", e)
            return (False, UNREACHABLE_MSG)

        if response.status_code == 200 :
            token = response.json().get("access_token")
            if token :
                self.token = token
                return (True, "")
            print("login: 200 response without access_token:", response.text)
            return (False, "Login failed. Please try again.")

        if response.status_code == 401 :
            return (False, "Invalid email or password.")

        print("login failed:", response.status_code, response.text)
        return (False, "Login failed. Please try again.")


    def signup(self, email, password) :

        try :
            response = requests.post(
                f"{BASE_URL}/auth/signup",
                json={
                    "email": email,
                    "password": password
                },
                timeout=TIMEOUT,
            )
        except requests.exceptions.RequestException as e :
            print("signup request failed:", e)
            return (False, UNREACHABLE_MSG)

        if response.status_code in (200, 201) :
            token = response.json().get("access_token")
            if token :
                self.token = token
            return (True, "")

        if response.status_code == 409 :
            return (False, "That email is already registered.")

        if response.status_code == 422 :
            return (False, "Please enter a valid email and password.")

        print("signup failed:", response.status_code, response.text)
        return (False, "Signup failed. Please try again.")
