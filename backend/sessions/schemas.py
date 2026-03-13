from pydantic import BaseModel

class SessionCreate(BaseModel) :
    scenario: str 