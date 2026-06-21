from pydantic import BaseModel


class ServiceCreate(BaseModel):
    name: str
    description: str
    duration_minutes: int


class ServiceResponse(BaseModel):
    id: int
    name: str
    description: str
    duration_minutes: int
    business_id: int

    class Config:
        from_attributes = True