from enum import Enum

class BookingStatus(str, Enum):
    """
    Represents the possible statuses of a booking in Slotify.
    """

    BOOKED = "BOOKED"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    NO_SHOW = "NO_SHOW"