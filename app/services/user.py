import uuid

from sqlmodel import Session, select

from app.schemas.transactions_db.user import User


# TODO: might move these later
class UserNotFound(Exception):
    """
    Raised when a user is not found in the database.
    """

    pass


class PermissionDenied(Exception):
    """
    Raised when a user is not authorized to perform an action.
    """

    pass


def create_user(db_session: Session, *, external_id: str) -> User:
    """
    Creates a new user, adds it to the session, and commits.
    Returns the newly created User object.
    """
    db_user = User(external_id=external_id)
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user


def get_user_by_external_id(db_session: Session, *, external_id: str) -> User | None:
    """
    Retrieves a user from the database by their external ID.
    Returns the User object or None if not found.
    """
    return db_session.exec(select(User).where(User.external_id == external_id)).first()


def delete_user(
    db_session: Session, *, user_id_to_delete: uuid.UUID, requesting_external_id: str
):
    """
    Deletes a user after verifying the requesting user has permission.
    Raises UserNotFound or PermissionDenied on failure.
    """
    # find the user to delete
    user_to_delete = db_session.get(User, user_id_to_delete)
    # raise an exception if the user does not exist
    if not user_to_delete:
        raise UserNotFound(f"User with id '{user_id_to_delete}' not found.")
    # raise an exception if the user is not authorized
    if user_to_delete.external_id != requesting_external_id:
        raise PermissionDenied("You do not have permission to delete this user.")
    # perform the deletion
    db_session.delete(user_to_delete)
    db_session.commit()
