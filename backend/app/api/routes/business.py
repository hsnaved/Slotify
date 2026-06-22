from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session 

from app.db.session import get_db
from app.schemas.business import BusinessCreate, BusinessResponse
from app.services.business_service import create_business_service
from app.api.deps import admin_only
from app.models.user import User



router = APIRouter()

@router.post("/business")
def create_business(
        business_data: BusinessCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(admin_only)
):
        """Create a new business owned by the authenticated `current_user`.

        The `admin_only` dependency is used to restrict this endpoint to
        users with administrative privileges.
        """
        return create_business_service(db, business_data, current_user)
