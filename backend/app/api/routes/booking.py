from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import (
    business_access,
    customer_only,
    get_current_user,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingDetailsResponse, BookingResponse
from app.services.booking_service import (
    cancel_booking_service,
    complete_booking_service,
    create_booking_service,
    get_my_bookings_service,
    get_owner_bookings_service,
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

@router.get(
    "/me",
    response_model=list[BookingDetailsResponse],
)
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(customer_only),
):
    """Return every booking created by the authenticated customer.

    The list is ordered from newest to oldest so the customer can review
    their recent appointments quickly.
    """

    return get_my_bookings_service(
        current_user=current_user,
        db=db,
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
    """Cancel an existing booking for the current user.

    The endpoint validates the caller's role and the cancellation window
    before allowing the booking to be cancelled.
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

    """Mark a booking as completed after the appointment has ended.

    Only an authenticated business owner or admin can complete a booking
    once the appointment time has passed.
    """
    
    return complete_booking_service(
        booking_id,
        current_user,
        db
    )

@router.get(
    "/owner/me",
    response_model=list[BookingDetailsResponse],
)
def get_owner_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(business_access),
):

    return get_owner_bookings_service(
        current_user=current_user,
        db=db,
    )