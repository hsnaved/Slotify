from pydantic import BaseModel

class BusinessCreate(BaseModel):
    name: str
    description: str

class BusinessResponse(BaseModel):
    id:  int
    name: str
    description: str
    owner_id: int

    class config:
        from_attributes = True
