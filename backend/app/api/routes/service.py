from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from app.db.session import get_db

from app.api.deps import business_access

from app.models.user import User

from app.services.service_service import create_service_service, get_owner_services_service, get_owner_slots_service, get_service_by_id_service, get_services_by_business_service
from app.services.service_service import get_available_slots_service
from app.schemas.availability_slot import AvailabilitySlotResponse
from app.schemas.services import(
    ServiceCreate,
    ServiceResponse,
    ServiceListResponse
)

router = APIRouter(prefix="/services", tags=["services"])

@router.post(
    "/businesses/{business_id}/services",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_service(
    business_id: int,
    service_data: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(business_access)
):
    """Create a new `Service` for the given `business_id`.

    The endpoint performs ownership and existence checks then
    delegates creation to `create_service_service`.
    """
    return create_service_service(
        business_id=business_id,
        service_data=service_data,
        current_user=current_user,
        db=db,
    )

@router.get(
    "/{service_id}",
    response_model=ServiceResponse
)
def get_service(
    service_id: int,
    db: Session = Depends(get_db),
):
    """Return the details of a single service by its identifier."""

    return get_service_by_id_service(
        service_id=service_id,
        db=db,
    )


@router.get(
    "/{business_id}/services",
    response_model=list[ServiceListResponse],
)
def get_business_services(
    business_id: int,
    db: Session = Depends(get_db),
):
    """Return all services offered by a specific business."""

    return get_services_by_business_service(
        business_id=business_id,
        db=db,
    )

@router.get(
    "/{service_id}/slots",
    response_model=list[AvailabilitySlotResponse],
)
def get_available_slots(
    service_id: int,
    db: Session = Depends(get_db),
):
    """Return all currently open availability slots for a given service."""

    return get_available_slots_service(
        service_id=service_id,
        db=db,
    )

@router.get(
    "/owner/me",
    response_model=list[ServiceResponse],
)
def get_owner_services(
    db: Session = Depends(get_db),
    current_user: User = Depends(business_access),
):
    """Return all services owned by the authenticated business owner."""

    return get_owner_services_service(
        current_user=current_user,
        db=db,
    )

@router.get(
    "/owner/slots",
    response_model=list[AvailabilitySlotResponse],
)
def get_owner_slots(
    db: Session = Depends(get_db),
    current_user: User = Depends(business_access),
):
    """Return all availability slots for the authenticated business owner's services."""

    return get_owner_slots_service(
        current_user=current_user,
        db=db,
    )