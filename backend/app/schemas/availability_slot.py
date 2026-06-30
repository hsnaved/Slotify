from pydantic import BaseModel
from datetime import datetime

class AvailabilitySlotResponse(BaseModel):

    id: int

    service_id: int

    start_datetime: datetime

    end_datetime: datetime

    is_booked: bool

    class Config:
        from_attributes = True