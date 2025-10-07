
class UserDirectoryAlreadyExists(Exception):
    """
    Raised when a user subdirectory is already found in the block image storage.

    example:
        path/to/{user_id} -> already exists
    """

    pass

class ImageAlreadyExists(Exception):
    """
    Raised when an image is already found in the block image storage.

    example:
        path/to/{user_id}/{storage_filename} -> already exists
    """

    pass

class ImageDirectoryAlreadyExists(Exception):
    """
    Raised when an image directory already found in the block image storage.

    example:
        path/to/{user_id}/{image_id} -> already exists
    """

    pass

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