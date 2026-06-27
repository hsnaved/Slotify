from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class GeneratedSlot:
    """
    Represents a generated availability slot before it is
    persisted into the database.

    Attributes:
        start_datetime:
            Slot start timestamp.

        end_datetime:
            Slot end timestamp.
    """

    start_datetime: datetime
    end_datetime: datetime