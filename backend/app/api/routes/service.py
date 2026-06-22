from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.db.session import get_db

from app.api.deps import admin_only

from app.models.user import User

from app.services.service_service import create_service_service
from app.schemas.services import(
    ServiceCreate,
    ServiceResponse
)

router = APIRouter(prefix="/services", tags=["services"])    

@router.post("/businesses/{business_id}/services", response_model = ServiceResponse)
def create_service(
    business_id: int,
    service_data: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
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