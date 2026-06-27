class BookingStatus(str, Enum):
    """
    Represents the possible statuses of a booking in Slotify.
    """

    BOOKED = "booked"
    PENDING = "pending"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"