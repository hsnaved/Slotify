from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session 

from app.db.session import get_db
from app.schemas.business import BusinessCreate, BusinessResponse
from app.services.business_service import create_business_service
from app.api.deps import business_access
from app.models.user import User



router = APIRouter(prefix="/businesses", tags=["businesses"])

@router.post("",response_model=BusinessResponse,
    status_code=status.HTTP_201_CREATED)
def create_business(
        business_data: BusinessCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(business_access)
):
        """Create a new business owned by the authenticated `current_user`.

        The `business_access` dependency is used to restrict this endpoint to
        users with administrative or ownership privileges.
        """
        return create_business_service(db, business_data, current_user)
