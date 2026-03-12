from fastapi import FastAPI
from backend.database.connection import engine 
from backend.database.models import Base 

app = FastAPI()

Base.metadata.create_all(engine)

@app.get("/")
def root():
    return{"message": "DriveSim API is running"}





