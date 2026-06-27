from enum import Enum


class WeekDay(str, Enum):
    """
    Represents valid weekdays for availability rules.

    Inheriting from `str` ensures that FastAPI/Pydantic
    serializes the enum values as strings in JSON.
    """

    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"