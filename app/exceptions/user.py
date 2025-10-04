# --- Custom Exceptions ---

class UserNotFound(Exception):
    """
    Raised when a user is not found in the database.
    """

    pass


class UserAlreadyExists(Exception):
    """
    Raised when a user is already in the database.
    """

    pass


class PermissionDenied(Exception):
    """
    Raised when a user is not authorized to perform an action.
    """

    pass