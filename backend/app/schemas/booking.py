from pydantic import BaseModel
from datetime import datetime

from app.enums.booking_status import BookingStatus

class BookingCreate(BaseModel):
    """
    Request model used to create a booking.
    """

    slot_id: int

class BookingResponse(BaseModel):
    """
    Response model returned after a booking is created.
    """

    id: int

    customer_id: int

    slot_id: int

    status: BookingStatus

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True

class BookingDetailsResponse(BaseModel):

    id: int

    status: BookingStatus

    slot_id: int

    customer_id: int

    class Config:
        from_attributes = True