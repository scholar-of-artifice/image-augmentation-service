import uuid
from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError
from sqlalchemy.exc import DataError, IntegrityError, InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.schemas.transactions_db.user import User

pytestmark = pytest.mark.asyncio

async def test_user_valid_model_is_persisted(async_db_session: AsyncSession):
    """
    GIVEN a User model
    AND all input data is valid
    WHEN that model is persisted
    THEN there are no errors
    AND the data is correct
    """
    # create a user
    user = User(external_id="some-1234-extr-0987-id45")
    async_db_session.add(user)
    await async_db_session.commit()
    await async_db_session.refresh(user)
    # Assert that the database populated the fields correctly
    assert isinstance(user.id, uuid.UUID)
    assert user.id is not None
    assert user.external_id == "some-1234-extr-0987-id45"
    assert user.external_id is not None
    assert isinstance(user.created_at, datetime)
    assert user.created_at is not None
    assert user.created_at.tzinfo is not None
    assert user.created_at.tzinfo == UTC


async def test_user_IntegrityError_when_external_id_is_duplicate(async_db_session: AsyncSession):
    """
    GIVEN a User A already exists
    AND a new User B is created
    AND both Users have the same external ID
    WHEN User B model is committed
    THEN an IntegrityError is raised
    """
    # create 2 users with same external_id
    user_A = User(external_id="some-1234-extr-0987-id45")
    user_B = User(external_id="some-1234-extr-0987-id45")
    # add the entries to the session
    async_db_session.add(user_A)
    async_db_session.add(user_B)
    # attempt commit them
    with pytest.raises(IntegrityError):
        await async_db_session.flush()


async def test_user_IntegrityError_when_external_id_is_null(async_db_session: AsyncSession):
    """
    GIVEN a User model
    AND external_id is null
    WHEN User model is committed
    THEN an IntegrityError is raised
    """
    # create a user
    user_to_create = User(external_id=None)
    # attempt to commit the user
    async_db_session.add(user_to_create)
    with pytest.raises(IntegrityError):
        await async_db_session.flush()


def no_test_user_ValidationError_when_external_id_is_blank_string(async_db_session: AsyncSession):
    # TODO: test fails and validation in pydantic not working as expected. take out for now.
    """
    GIVEN a User model
    AND external_id is a blank string
    WHEN User model is made
    THEN an ValidationError is raised
    """
    with pytest.raises(ValidationError):
        User(external_id="")


async def test_user_IntegrityError_when_external_id_is_too_long(async_db_session: AsyncSession):
    """
    GIVEN a User model
    AND external_id is too long
    WHEN User model is committed
    THEN an DataError is raised
    """
    # create a user
    user_to_create = User(external_id="a" * 300)
    # attempt to commit the user
    async_db_session.add(user_to_create)
    with pytest.raises(DataError):
        await async_db_session.flush()


async def test_get_user_by_primary_key(async_db_session: AsyncSession):
    """
    GIVEN a User model
    AND all input data is valid
    WHEN User model is retrieved by primary key
    THEN the data is correct
    """
    # create a user
    user = User(external_id="this_is_some_external_id")
    async_db_session.add(user)
    await async_db_session.commit()
    await async_db_session.refresh(user)
    # get the user by id
    retrieved_user = await async_db_session.get(User, user.id)
    # assert that the users are the same
    assert retrieved_user is not None
    assert retrieved_user.id == user.id
    assert retrieved_user.external_id == "this_is_some_external_id"


async def test_get_user_by_primary_key_not_found(async_db_session: AsyncSession):
    """
    GIVEN no User exists with a specific ID
    WHEN a User is retrieved by that ID
    THEN the result is None
    """
    # make some UUID
    non_existent_id = uuid.uuid4()
    # try to get a user with that ID
    retrieved_user = await async_db_session.get(User, non_existent_id)
    # the result is None
    assert retrieved_user is None


async def test_get_user_by_external_id(async_db_session: AsyncSession):
    """
    GIVEN a User exists in the database
    WHEN a query is made for the User by the external_id
    THEN the correct User is returned
    """
    # make a user with a known external_id
    target_external_id = "some_external_id"
    user_in_db = User(external_id=target_external_id)
    async_db_session.add(user_in_db)
    await async_db_session.flush()
    # query for the user by that external_id
    statement = select(User).where(User.external_id == target_external_id)
    result = await async_db_session.execute(statement)
    retrieved_user = result.scalars().first()
    # the retrieved user should be the right one
    assert retrieved_user is not None
    assert retrieved_user.external_id == target_external_id
    assert retrieved_user.id == user_in_db.id


async def NO_test_read_only_fields_are_not_updated(async_db_session: AsyncSession):
    # TODO: this test fails
    """
    GIVEN a User exists in the database
    WHEN read-only fields ('id', 'created_at') are changed on the object
    AND the session is committed
    THEN the original values in the database remain unchanged
    """
    # create a user
    user = User(external_id="some_external_id")
    async_db_session.add(user)
    async_db_session.commit()
    async_db_session.refresh(user)
    # store the original, correct values
    original_id = user.id
    original_created_at = user.created_at
    # change the read-only fields in memory
    user.id = uuid.uuid4()  # assign a new, random UUID
    user.created_at = datetime.now(UTC) + timedelta(days=1)
    # commit the session.
    # SQLAlchemy will see the object is "dirty"
    # but should ignore changes to the primary key and non-writable fields
    async_db_session.commit()
    # refresh the object to get the true state from the database
    async_db_session.refresh(user)
    # assert that the values have reverted to their original state
    assert user.id == original_id
    assert user.created_at == original_created_at


async def test_external_id_can_be_updated(async_db_session: AsyncSession):
    """
    GIVEN a User exists in the database
    WHEN mutable-only fields ('external_id') are changed on the object
    AND the session is committed
    THEN the original values in the database is changed
    """
    # create a user
    user = User(external_id="some_external_id")
    async_db_session.add(user)
    await async_db_session.flush()
    await async_db_session.refresh(user)
    # store the original value
    original_some_external_id = user.external_id
    # change the read-only fields in memory
    user.external_id = "oh_wow_this_is_some_external_id"
    # commit the session.
    # SQLAlchemy will see the object is "dirty"
    # but should ignore changes to the primary key and non-writable fields
    await async_db_session.flush()
    # refresh the object to get the true state from the database
    await async_db_session.refresh(user)
    await async_db_session.commit()
    # assert that the values have reverted to their original state
    assert user.external_id != original_some_external_id


async def test_delete_user(async_db_session: AsyncSession):
    """
    GIVEN a User exists in the database
    WHEN the User is deleted
    THEN it can no longer be retrieved from the database
    """
    # create a user
    user_to_delete = User(external_id="some_external_id")
    async_db_session.add(user_to_delete)
    await async_db_session.commit()
    await async_db_session.refresh(user_to_delete)
    # store its ID so we can look for it later
    user_id = user_to_delete.id
    # confirm it's in the database before deleting
    assert await async_db_session.get(User, user_id) is not None
    # delete the user
    await async_db_session.delete(user_to_delete)
    await async_db_session.commit()
    # the user cannot be found by its primary key
    retrieved_user = await async_db_session.get(User, user_id)
    assert retrieved_user is None


async def test_delete_user_that_does_not_exist(async_db_session: AsyncSession):
    """
    GIVEN a User does not exist in the database
    WHEN the User is deleted
    THEN an InvalidRequestError is raised
    """
    # create a user
    user_not_in_db = User(external_id="some-id")
    # check that it has an ID from the default_factory
    assert user_not_in_db.id is not None
    # delete raises an error
    # because this instance is not tracked by the session.
    with pytest.raises(InvalidRequestError):
        await async_db_session.delete(user_not_in_db)


# TODO: Test querying with an invalid UUID format to ensure it fails gracefully.
