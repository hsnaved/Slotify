from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.api.deps import business_access

from app.models.user import User

from app.schemas.availability_rule import (
    AvailabilityRuleCreate,
    AvailabilityRuleResponse
)

from app.services.availability_rule_service import (
    create_availability_rule_service
)

router = APIRouter(
    prefix="/services",
    tags=["availability-rules"]
)


@router.post(
    "/{service_id}/availability-rules",
    response_model=AvailabilityRuleResponse,
    status_code=status.HTTP_201_CREATED
)

def create_availability_rule(
    service_id: int,
    rule_data: AvailabilityRuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(business_access)
):
    """Create a new availability rule for a service owned by the authenticated `current_user`.

    The `business_access` dependency is used to restrict this endpoint to
    users with administrative or ownership privileges.
    """
    return create_availability_rule_service(
        service_id=service_id,
        rule_data=rule_data,
        current_user=current_user,
        db=db
    )