
class UserDirectoryNotFound(Exception):
    """
    Raised when a user sub-directory is not found in the database.

    example:
        path/to/{user_id} -> does not exist
    """

    pass