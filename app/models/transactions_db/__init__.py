# Runtime Model Discovery
# A more robust, long-term solution is to create an __init__.py file in your models directory that imports all your models.
# This turns your models folder into a package that pre-loads all tables.

from .user import User
from .unprocessed_image import UnprocessedImage