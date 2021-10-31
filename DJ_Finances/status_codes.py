from enum import Enum

class StatusCode(Enum):
    """This enum exists to avoid comparison to magic numbers in the tests."""
    OK = 200
    CREATED = 201
    FORBIDDEN = 403
    NOT_FOUND = 404