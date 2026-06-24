from datetime import date, time
from proto import Enum
from pydantic import BaseModel



class WeekDay(str, Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"
    
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