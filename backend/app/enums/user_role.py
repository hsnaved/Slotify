from enum import Enum


class UserRole(str, Enum):
    """
    Represents the supported user roles within Slotify.
    """

    ADMIN = "admin"
    OWNER = "owner"
    CUSTOMER = "customer"
