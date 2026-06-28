from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import (
    business_access,
    customer_only,
    get_current_user,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingResponse
from app.services.booking import (
    cancel_booking_service,
    complete_booking_service,
    create_booking_service,
)


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.post(
    "",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED
)
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(customer_only)
):
    """
    Creates a booking for an available slot.

    Only authenticated customers are allowed
    to create bookings.
    """

    return create_booking_service(
        booking_data=booking_data,
        current_user=current_user,
        db=db
    )

@router.patch(
    "/{booking_id}/cancel",
    response_model=BookingResponse
)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cancels an existing booking.
    """

    return cancel_booking_service(
        booking_id,
        current_user,
        db
    )

@router.patch(
    "/{booking_id}/complete",
    response_model=BookingResponse
)
def complete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(business_access)
):

    """
    Marks a booking as completed.
    """
    
    return complete_booking_service(
        booking_id,
        current_user,
        db
    )