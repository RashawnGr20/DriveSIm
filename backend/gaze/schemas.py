from pydantic import BaseModel
from typing import List

class GazeCreate(BaseModel) :
    pose: str
    yaw: float
    pitch: float
    duration: float


class GazeBatchCreate(BaseModel) :
    session_id: int
    events : List[GazeCreate]