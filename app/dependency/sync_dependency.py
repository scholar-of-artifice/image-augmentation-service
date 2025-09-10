from fastapi import Depends, HTTPException, status
from app.schemas.transactions_db.user import User
from app.db.database import get_session
from sqlmodel import Session, select
from app.dependency.async_dependency import get_current_external_user_id

def get_current_active_user(
        *,
        external_id: str = Depends(get_current_external_user_id),
        db_session: Session = Depends(get_session)
) -> User:
    """
        Gets the external_id from the token...
        finds the user in the database...
        and returns the complete User model object.
    """
    user = db_session.exec(select(User).where(User.external_id == external_id)).first()
    if not user:
        # this protects against cases where a valid token is presented for a user who has since been deleted from our database.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    return user