from pydantic import BaseModel


class BusinessCreate(BaseModel):
    """Request schema for creating a new business."""
    name: str
    description: str


class BusinessResponse(BaseModel):
    """Response schema for a business entity.

    The nested `Config` (note: originally declared as `config` in the
    codebase) instructs Pydantic how to serialize ORM model instances.
    """
    id: int
    name: str
    description: str
    owner_id: int

    class config:
        # NOTE: this is lowercase `config` which is non-standard for
        # Pydantic. The canonical name is `Config`. This comment keeps
        # the original behaviour while flagging the intended usage.
        from_attributes = True

class BusinessListResponse(BaseModel):
    """
    Business information shown to customers.
    """

    id: int

    name: str

    description: str
    
    class Config:
        from_attributes = True
    
