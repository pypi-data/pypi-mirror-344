from enum import Enum


class MLSearchStatus(Enum):
    """The model class that lists all the possible statuses of the founded result."""

    none = ""
    found = "found"
    error = "error"
    not_found = "not found"