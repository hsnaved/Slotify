from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.business_settings import BusinessSettings
from app.models.user import User
from app.enums.user_role import UserRole

from app.schemas.business_settings import (
    BusinessSettingsUpdate,
)

def get_business_settings_service(
    business_id: int,
    current_user: User,
    db: Session,
) -> BusinessSettings:
    """
    Returns the settings for a business.

    Only the owner of the business or
    an administrator can access them.
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

    if (
        current_user.role != UserRole.ADMIN
        and business.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to access these settings."
        )

    return business.settings

def update_business_settings_service(
    business_id: int,
    settings_data: BusinessSettingsUpdate,
    current_user: User,
    db: Session,
) -> BusinessSettings:
    """
    Updates the configurable settings
    of a business.

    Only the business owner or an
    administrator may perform this action.
    """

    try:

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

        if (
           current_user.role != UserRole.ADMIN
            and business.owner_id != current_user.id
        ):
            raise HTTPException(
                status_code=403,
                detail="You are not allowed to update these settings."
            )

        settings = business.settings

        for field, value in (
            settings_data.model_dump(
                exclude_unset=True
            ).items()
        ):
            setattr(settings, field, value)

        db.commit()

        db.refresh(settings)

        return settings

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Unable to update business settings."
        )