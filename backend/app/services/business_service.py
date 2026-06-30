from http.client import HTTPException

from sqlalchemy.orm import Session

from app.schemas.business import BusinessCreate
from app.models.business import Business
from app.models.business_settings import BusinessSettings
from app.models.user import User


def create_business_service(
    db: Session,
    business_data: BusinessCreate,
    user: User,
):
    """Create and persist a new `Business` owned by `user`.

    Returns the newly created `Business` model after committing the
    transaction.
    """

    business = Business(
        name=business_data.name,
        description=business_data.description,
        owner_id=user.id,
    )

    db.add(business)
    db.flush()

    settings = BusinessSettings(
        business_id=business.id
    )
    db.add(settings)

    db.commit()
    db.refresh(business)
    return business

def get_owner_business_service(
    current_user: User,
    db: Session,
):
    """Fetch the business owned by the authenticated user.

    Raises an HTTP 404 error when no business has been created for the user.
    """

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

    return business



def get_all_businesses_service(
    db: Session,
):
    """
    Returns all registered businesses for customers.
    """

    businesses = (
    db.query(Business)
    .order_by(Business.name)
    .all()
    )

    return businesses