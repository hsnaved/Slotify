from pydantic import BaseModel


class ServiceCreate(BaseModel):
    """Request schema for creating a new service.

    Fields correspond to the attributes required to create a `Service`.
    """
    name: str
    description: str
    duration_minutes: int


class ServiceResponse(BaseModel):
    """Response schema for a service.

    This schema is used to serialize `Service` model instances returned
    by API endpoints.
    """
    id: int
    name: str
    description: str
    duration_minutes: int
    business_id: int

    class Config:
        # `from_attributes` instructs Pydantic to read attributes from
        # objects (e.g. ORM models) when creating the schema. Depending
        # on the Pydantic version you use this may be `orm_mode = True`
        # or `from_attributes = True`.
        from_attributes = True

class ServiceListResponse(BaseModel):
    """
    Service information displayed to customers.
    """

    id: int
    name: str
    description: str
    duration_minutes: int
    
    class Config:
        from_attributes = True