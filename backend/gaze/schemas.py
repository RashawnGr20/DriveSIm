from pydantic import BaseModel
from typing import List 

def GazeCreate(BaseModel) : 
    pose: str 
    yaw: float
    pitch: float 
    duration: float 


def GazeBatchCreate(BaseModel) : 
    session_id: int
    events : List[GazeCreate]