from datetime import date, time
from enum import Enum
from pydantic import BaseModel
from app.enums.weekdays import WeekDay

class AvailabilityRuleCreate(BaseModel):
    start_date: date
    end_date: date

    weekdays: list[WeekDay]

    start_time: time
    end_time: time


class AvailabilityRuleResponse(BaseModel):
    id: int

    service_id: int

    start_date: date
    end_date: date

    weekdays: list[WeekDay]

    start_time: time
    end_time: time

    class Config:
        from_attributes = True