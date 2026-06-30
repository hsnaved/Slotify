from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.enums.cancellation_policy import CancellationPolicy


class BusinessSettingsResponse(BaseModel):
    """
    Response schema for business settings.
    """

    id: int

    business_id: int

    requires_booking_approval: bool

    customer_cancellation_window_minutes: int

    allow_customer_cancellation: bool

    allow_owner_cancellation: bool

    cancellation_policy: CancellationPolicy

    timezone: str

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True

class BusinessSettingsUpdate(BaseModel):
    """
    Schema used by owners to update
    their business settings.
    """

    requires_booking_approval: Optional[bool] = None

    customer_cancellation_window_minutes: Optional[int] = None

    allow_customer_cancellation: Optional[bool] = None

    allow_owner_cancellation: Optional[bool] = None

    cancellation_policy: Optional[CancellationPolicy] = None

    timezone: Optional[str] = None