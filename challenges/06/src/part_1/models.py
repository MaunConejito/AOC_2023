from pydantic import BaseModel

class Race(BaseModel):
    time: int
    record: int