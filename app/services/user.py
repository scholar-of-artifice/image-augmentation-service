from sqlmodel import Session, select
from app.schemas.transactions_db.user import User

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
