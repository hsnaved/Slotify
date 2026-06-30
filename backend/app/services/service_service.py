from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.service import Service
from app.models.availability_slot import AvailabilitySlot
from app.models.user import User
from datetime import datetime

from app.schemas.services import ServiceCreate

def create_service_service(
        business_id: int,
        service_data: ServiceCreate,
        current_user: User,
        db: Session
):
    """Create a new service for `business_id` if authorized.

    Performs an existence check for the target `Business`, verifies the
    `current_user` owns the business (authorization), creates the
    `Service` and returns the persisted model instance.
    """
    business = db.query(Business).filter(
            Business.id == business_id
        ).first()
    
    if not business:
        raise HTTPException(
            status_code = 404,
            detail = "Business not found"
        )
    
    # Ownership check: ensure the authenticated user owns the business
    # before allowing creation of a nested Service.
    if business.owner_id != current_user.id:
        raise HTTPException(
            status_code = 403,
            detail = "Not authorized to create service for this business"
        )
    
    service = Service(
        name = service_data.name,
        description = service_data.description,
        duration_minutes = service_data.duration_minutes,
        business_id = business_id
    )

    db.add(service)
    db.commit()
    db.refresh(service)

    return service

def get_service_by_id_service(
    service_id: int,
    db: Session,
) -> Service:
    """Fetch a single service by its database identifier.

    Raises an HTTP 404 error when no matching service exists.
    """

    service = (
        db.query(Service)
        .filter(Service.id == service_id)
        .first()
    )

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found."
        )

    return service


def get_services_by_business_service(
    business_id: int,
    db: Session,
):
    """Return every service belonging to a specific business.

    The result is ordered by service name for easier browsing.
    """

    business = (
        db.query(Business)
        .filter(Business.id == business_id)
        .first()
    )

    if business is None:
        raise HTTPException(
            status_code=404,
            detail="Business not found."
        )

    return (
        db.query(Service)
        .filter(
            Service.business_id == business_id
        )
        .order_by(Service.name)
        .all()
    )

def get_owner_services_service(
    current_user: User,
    db: Session,
):
    """Return all services for the authenticated business owner's business."""

    business = (
        db.query(Business)
        .filter(
            Business.owner_id == current_user.id
        )
        .first()
    )

    if business is None:
        raise HTTPException(
            status_code=404,
            detail="Business not found."
        )

    return (
        db.query(Service)
        .filter(
            Service.business_id == business.id
        )
        .all()
    )

def get_available_slots_service(
    service_id: int,
    db: Session,
):
    """Return all future unbooked slots for a service.

    Slots are filtered to exclude already booked and past appointments.
    """

    service = (
        db.query(Service)
        .filter(Service.id == service_id)
        .first()
    )

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found."
        )

    return (
        db.query(AvailabilitySlot)
        .filter(
            AvailabilitySlot.service_id == service_id,
            AvailabilitySlot.is_booked == False,
            AvailabilitySlot.start_datetime > datetime.utcnow(),
        )
        .order_by(
            AvailabilitySlot.start_datetime
        )
        .all()
    )

def get_owner_slots_service(
    current_user: User,
    db: Session,
):
    """Return all availability slots for services owned by the current user."""

    return (
        db.query(AvailabilitySlot)
        .join(Service)
        .join(Business)
        .filter(
            Business.owner_id == current_user.id
        )
        .order_by(
            AvailabilitySlot.start_datetime
        )
        .all()
    )