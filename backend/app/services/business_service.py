from sqlalchemy.orm import Session

from app.schemas.business import BusinessCreate
from app.models.business import Business
from app.models.user import User



def create_business_service(
        db:Session,
        business_data: BusinessCreate,
        user:User
):
    
    business = Business(
        name = business_data.name,
        description = business_data.description,
        owner_id = user.id
    )

    db.add(business)
    db.commit()
    db.refresh(business)
    return business