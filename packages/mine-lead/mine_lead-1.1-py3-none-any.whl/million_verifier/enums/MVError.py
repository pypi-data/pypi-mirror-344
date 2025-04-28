from enum import Enum


class MVError(Enum):
    """The model class that lists all the possible statuses of the founded result."""

    none = ""
    apikey_not_found = "apikey_not_found"
    no_email = "No email specified"
    unknown = "unknown"