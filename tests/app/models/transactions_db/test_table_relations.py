from sqlmodel import Session
from app.models.transactions_db.user import User
from app.models.transactions_db.unprocessed_image import UnprocessedImage

# TODO: write a test which enforces the relationship between User and UnprocessedImage

# TODO: write a test which enforces the relationship between User and ProcessedImage

# TODO: write a test which enforces the relationship between UnprocessedImage and ProcessedImage

# TODO: write a test which enforces the relationship between ProcessingJob and User

# TODO: write a test which enforces the relationship between ProcessingJob and UnprocessedImage

# TODO: write a test which enforces the relationship between ProcessingJob and ProcessedImage

# TODO: Test that creating an image with a valid user_id correctly populates the relationship attributes.

# TODO: Test that after creating an image, the user's list of images is correctly updated.

# TODO: Test linking by assigning the parent object directly, instead of using the foreign key ID.

# TODO: Test linking by appending an image to the user's list of images.

# --- TODOs for Constraint & Deletion Violations ---

# TODO: Test that the foreign key constraint prevents creating an image with a fake user_id.

# TODO: Test that the database prevents a user from being deleted if they still have images.

# TODO: Test that deleting an image does not affect its parent user.
