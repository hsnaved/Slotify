from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.enums.weekdays import WeekDay
from app.models.availability_rule import AvailabilityRule
from app.models.availability_slot import AvailabilitySlot
from app.models.service import Service
from app.models.user import User
from app.schemas.availability_rule import AvailabilityRuleCreate
from app.utils.slot_generator import generate_slots_for_rule


def create_availability_rule_service(
    service_id: int,
    rule_data: AvailabilityRuleCreate,
    current_user: User,
    db: Session
) -> AvailabilityRule:
    """
    Creates an availability rule for a service and automatically
    generates all availability slots.

    Workflow:
        1. Validate service existence.
        2. Validate ownership.
        3. Validate request data.
        4. Persist availability rule.
        5. Generate slots.
        6. Persist generated slots.
        7. Commit transaction.

    Args:
        service_id:
            ID of the service.

        rule_data:
            Availability rule submitted by the business owner.

        current_user:
            Authenticated user.

        db:
            Active SQLAlchemy database session.

    Returns:
        AvailabilityRule:
            Newly created availability rule.

    Raises:
        HTTPException:
            400 -> Invalid request.
            403 -> Unauthorized.
            404 -> Service not found.
    """

    # ---------------------------------------------------------
    # Validate Service
    # ---------------------------------------------------------

    service = (
        db.query(Service)
        .filter(Service.id == service_id)
        .first()
    )

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found."
        )

    # ---------------------------------------------------------
    # Validate Ownership
    # ---------------------------------------------------------

    if service.business.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to manage this service."
        )

    # ---------------------------------------------------------
    # Business Validations
    # ---------------------------------------------------------

    if rule_data.start_date > rule_data.end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be after end date."
        )

    if rule_data.start_time >= rule_data.end_time:
        raise HTTPException(
            status_code=400,
            detail="Start time must be earlier than end time."
        )

    if len(rule_data.weekdays) == 0:
        raise HTTPException(
            status_code=400,
            detail="Select at least one weekday."
        )

    if service.duration_minutes <= 0:
        raise HTTPException(
            status_code=400,
            detail="Service duration must be greater than zero."
        )

    try:

        # ---------------------------------------------------------
        # Create Availability Rule
        # ---------------------------------------------------------

        rule = AvailabilityRule(
            service_id=service.id,
            start_date=rule_data.start_date,
            end_date=rule_data.end_date,
            weekdays=[
                day.value
                for day in rule_data.weekdays
            ],
            start_time=rule_data.start_time,
            end_time=rule_data.end_time
        )

        db.add(rule)

        # Flush so rule.id gets generated without committing
        db.flush()

        # ---------------------------------------------------------
        # Generate Slots
        # ---------------------------------------------------------

        generated_slots = generate_slots_for_rule(
            start_date=rule.start_date,
            end_date=rule.end_date,
            weekdays=[
                WeekDay(day)
                for day in rule.weekdays
            ],
            start_time=rule.start_time,
            end_time=rule.end_time,
            duration_minutes=service.duration_minutes
        )

        # ---------------------------------------------------------
        # Convert Generated Slots -> ORM Objects
        # ---------------------------------------------------------

        availability_slots = []

        for generated_slot in generated_slots:

            availability_slots.append(
                AvailabilitySlot(
                    service_id=service.id,
                    rule_id=rule.id,
                    start_datetime=generated_slot.start_datetime,
                    end_datetime=generated_slot.end_datetime,
                    is_booked=False
                )
            )

        # ---------------------------------------------------------
        # Bulk Insert
        # ---------------------------------------------------------

        db.add_all(availability_slots)

        # ---------------------------------------------------------
        # Commit Transaction
        # ---------------------------------------------------------

        db.commit()

        db.refresh(rule)

        return rule

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while creating the availability rule: {str(e)}"
        )