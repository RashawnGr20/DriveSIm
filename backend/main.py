from fastapi import FastAPI
from backend.database.connection import engine 
from backend.database.models import Base 
from backend.auth.router import router as auth_router
from backend.sessions.router import router as session_router

app = FastAPI()

Base.metadata.create_all(engine)

@app.get("/")
def root():
    return{"message": "DriveSim API is running"}

app.include_router(auth_router)
app.include_router(session_router)






