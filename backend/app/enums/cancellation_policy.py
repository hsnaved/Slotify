from enum import Enum


class CancellationPolicy(str, Enum):
    """
    Determines what happens to a slot
    when a booking is cancelled.
    """

    REOPEN_SLOT = "REOPEN_SLOT"
    KEEP_SLOT_BLOCKED = "KEEP_SLOT_BLOCKED"