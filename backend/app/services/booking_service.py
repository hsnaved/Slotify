from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.enums.booking_status import BookingStatus
from app.enums.cancellation_policy import CancellationPolicy
from app.models.availability_slot import AvailabilitySlot
from app.models.booking import Booking
from app.models.service import Service
from app.models.business import Business
from app.models.user import User
from app.schemas.booking import BookingCreate
from app.enums.user_role import UserRole
from datetime import datetime, timedelta


def create_booking_service(
    booking_data: BookingCreate,
    current_user: User,
    db: Session
) -> Booking:
    """
    Creates a booking for an available slot.

    Workflow:
        1. Validate slot exists.
        2. Lock the slot row to prevent concurrent bookings.
        3. Ensure the slot is still available.
        4. Create the booking.
        5. Mark the slot as booked.
        6. Commit the transaction.

    Args:
        booking_data:
            Incoming booking request.

        current_user:
            Authenticated customer.

        db:
            Active SQLAlchemy database session.

    Returns:
        Booking:
            Newly created booking.

    Raises:
        HTTPException:
            404 -> Slot not found.

        HTTPException:
            409 -> Slot already booked.

        HTTPException:
            500 -> Unexpected server error.
    """

    try:
        # ---------------------------------------------------------
        # Acquire a row-level lock on the slot.
        #
        # This prevents multiple customers from booking the same
        # slot simultaneously (Pessimistic Locking).
        # ---------------------------------------------------------
        availability_slot = (
            db.query(AvailabilitySlot)
            .filter(
                AvailabilitySlot.id == booking_data.slot_id
            )
            .with_for_update()
            .first()
        )

        # ---------------------------------------------------------
        # Validate slot exists
        # ---------------------------------------------------------
        if availability_slot is None:
            raise HTTPException(
                status_code=404,
                detail="Slot not found."
            )

        # ---------------------------------------------------------
        # Ensure the slot is available
        # ---------------------------------------------------------
        if availability_slot.is_booked:
            raise HTTPException(
                status_code=409,
                detail="This slot has already been booked."
            )

        # ---------------------------------------------------------
        # Create booking
        # (Future enhancement:
        # Business may require approval, in which case
        # status = BookingStatus.PENDING)
        # ---------------------------------------------------------
        settings = availability_slot.service.business.settings

        booking_status = (
            BookingStatus.PENDING
            if settings.requires_booking_approval
            else BookingStatus.BOOKED
        )
        
        booking = Booking(
            customer_id=current_user.id,
            slot_id=availability_slot.id,
            status=booking_status
        )

        db.add(booking)

        # ---------------------------------------------------------
        # Mark slot as unavailable
        # ---------------------------------------------------------
        availability_slot.is_booked = True

        # ---------------------------------------------------------
        # Commit transaction
        # ---------------------------------------------------------
        db.commit()

        db.refresh(booking)

        return booking

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="This slot has already been booked."
        )

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Unable to create booking. Please try again."
        )
    

def cancel_booking_service(
    booking_id: int,
    current_user: User,
    db: Session
) -> Booking:
    """
    Cancels a booking.

    Rules:
        - Customer can cancel only their own booking.
        - Customer can cancel only up to 30 minutes
          before the appointment.
        - Owner can cancel bookings belonging
          to their business.
        - Admin can cancel any booking.
    """

    try:

        booking = (
            db.query(Booking)
            .filter(Booking.id == booking_id)
            .first()
        )

        if booking is None:
            raise HTTPException(
                status_code=404,
                detail="Booking not found."
            )

        if booking.status == BookingStatus.CANCELLED:
            raise HTTPException(
                status_code=409,
                detail="Booking already cancelled."
            )

        slot = booking.slot
        settings = (
            slot
            .service
            .business
            .settings
        )

        # --------------------------------------------------
        # CUSTOMER
        # --------------------------------------------------

        if current_user.role == UserRole.CUSTOMER:

            if booking.customer_id != current_user.id:
                raise HTTPException(
                    status_code=403,
                    detail="You cannot cancel another customer's booking."
                )

            window = settings.customer_cancellation_window_minutes
            cancellation_deadline = (
                slot.start_datetime - timedelta(minutes=window)
            )

            if datetime.utcnow() > cancellation_deadline:
                raise HTTPException(
                    status_code=400,
                    detail="Bookings can only be cancelled at least 30 minutes before the appointment."
                )

        # --------------------------------------------------
        # OWNER
        # --------------------------------------------------

        elif current_user.role == UserRole.OWNER:

            if (
                slot.service.business.owner_id
                != current_user.id
            ):
                raise HTTPException(
                    status_code=403,
                    detail="You do not own this booking."
                )

        # --------------------------------------------------
        # ADMIN
        # --------------------------------------------------

        booking.status = BookingStatus.CANCELLED

        if (settings.cancellation_policy == CancellationPolicy.REOPEN_SLOT):
            slot.is_booked = False

        db.commit()

        db.refresh(booking)

        return booking

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Unable to cancel booking."
        )
    

def complete_booking_service(
    booking_id: int,
    current_user: User,
    db: Session
) -> Booking:
    """
    Marks a booking as completed.

    Only the business owner (or platform admin)
    can complete a booking.
    """

    try:

        booking = (
            db.query(Booking)
            .filter(
                Booking.id == booking_id
            )
            .first()
        )

        if booking is None:
            raise HTTPException(
                status_code=404,
                detail="Booking not found."
            )

        slot = booking.slot

        # ---------------- OWNER -----------------

        if current_user.role == UserRole.OWNER:

            if (
                slot.service.business.owner_id
                != current_user.id
            ):
                raise HTTPException(
                    status_code=403,
                    detail="You do not own this booking."
                )

        # ---------------- STATUS ----------------

        if booking.status != BookingStatus.BOOKED:
            raise HTTPException(
                status_code=409,
                detail="Only booked appointments can be completed."
            )

        if datetime.utcnow() < slot.end_datetime:
            raise HTTPException(
                status_code=400,
                detail="Appointment has not finished yet."
            )

        booking.status = BookingStatus.COMPLETED

        db.commit()

        db.refresh(booking)

        return booking

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Unable to complete booking."
        )
    
def get_my_bookings_service(
    current_user: User,
    db: Session,
):
    """Return all bookings belonging to the authenticated customer."""

    return (
        db.query(Booking)
        .filter(
            Booking.customer_id == current_user.id
        )
        .order_by(
            Booking.created_at.desc()
        )
        .all()
    )

def get_owner_bookings_service(
    current_user: User,
    db: Session,
):
    """Return all bookings associated with the authenticated business owner."""

    return (
        db.query(Booking)
        .join(AvailabilitySlot)
        .join(Service)
        .join(Business)
        .filter(
            Business.owner_id == current_user.id
        )
        .order_by(
            Booking.created_at.desc()
        )
        .all()
    )