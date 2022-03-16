from pydantic import BaseModel

class Secret(BaseModel):
    id:int
    gender:str
    age:int
    secret:str