
class UserDirectoryNotFound(Exception):
    """
    Raised when a user sub-directory is not found in the database.

    example:
        path/to/{user_id} -> does not exist
    """

    pass


class ImageDirectoryNotFound(Exception):
    """
    Raised when an image sub-directory is not found in the database.

    example:
        path/to/{user_id}/{image_id} -> does not exist
    """

    pass