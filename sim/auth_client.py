import requests 

BASE_URL = "http://127.0.0.1:8000"

class AuthClient : 

    def __init__(self):
        self.token = None 
    

    def login(self, email, password ) : 

        response = requests.post(
            f"{BASE_URL}/auth/login",
        json={
            "email": email, 
            "password": password
            }
        )

        
        if response.status_code == 200 : 
            data = response.json()
            self.token = data["access_token"]
            return True 


    def signup(self, email, password) : 

        response = requests.post(
            f"{BASE_URL}/auth/signup",
        json={
            "email": email, 
            "password": password
            }
        )

        

        return response.status_code == 200 