from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.service import Service
from app.models.user import User

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
    