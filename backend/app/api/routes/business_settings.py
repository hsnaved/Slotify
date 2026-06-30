from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.api.deps import business_access
from app.db.session import get_db

from app.models.user import User

from app.schemas.business_settings import (
    BusinessSettingsResponse,
    BusinessSettingsUpdate,
)

from app.services.business_settings_service import (
    get_business_settings_service,
    update_business_settings_service,
)

router = APIRouter(
    prefix="/businesses",
    tags=["Business Settings"],
)

@router.get(
    "/{business_id}/settings",
    response_model=BusinessSettingsResponse,
)

def get_business_settings(
    business_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(business_access),
):
    """Return the configuration settings for a specific business."""

    return get_business_settings_service(
        business_id=business_id,
        current_user=current_user,
        db=db,
    )

@router.patch(
    "/{business_id}/settings",
    response_model=BusinessSettingsResponse,
)
def update_business_settings(
    business_id: int,
    settings_data: BusinessSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(business_access),
):
    """Update one or more configurable settings for a specific business."""

    return update_business_settings_service(
        business_id=business_id,
        settings_data=settings_data,
        current_user=current_user,
        db=db,
    )