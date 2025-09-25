import uuid

from fastapi import status
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
from app.schemas.transactions_db.user import User

pytestmark = pytest.mark.asyncio

# CREATE USER


async def test_create_user_success(async_client: AsyncClient):
    """
    GIVEN an external_user_id
    WHEN the POST request is made to create a new user
    THEN check the response is valid
    """
    # define the header for a new, unique user
    headers = {"X-External-User-ID": "new-user-123"}
    # make the POST request to the endpoint
    response = await async_client.post(url="/users-api/users", headers=headers)
    # check the results
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["external_id"] == "new-user-123"
    assert "id" in data
    assert data["id"] is not None
    assert "created_at" in data
    assert data["created_at"] is not None


async def test_create_user_raises_conflict_when_user_already_exists(async_client: AsyncClient):
    """
    GIVEN an external_id
    AND a user with the same external_id already exists
    WHEN the POST request is made to create a new user
    THEN it returns 409
    """
    # create a user
    headers = {"X-External-User-ID": "existing-user-456"}
    response = await async_client.post(url="/users-api/users", headers=headers)
    # this first call should succeed
    assert response.status_code == status.HTTP_201_CREATED
    # attempt to create the same user again
    response = await async_client.post(url="/users-api/users", headers=headers)
    # check for the conflict error
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {
        "detail": "User with external_id 'existing-user-456' already exists."
    }


async def test_create_user_raises_unauthorized_when_user_is_not_authorized(
    async_client: AsyncClient,
):
    """
    GIVEN an external_id
    AND a user with the same external_id already exists
    WHEN the POST request is made to create a new user
    THEN it returns 401
    """
    # create a user
    headers = {"X-External-User-ID": ""}
    # make the request
    response = await async_client.post(url="/users-api/users", headers=headers)
    # check the failure
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Missing X-External-User-ID header"}


# SIGN IN USER


async def test_sign_in_user_success(async_client: AsyncClient, async_db_session: AsyncSession):
    """
    GIVEN an active user exists in the database
    WHEN a POST request is made to /sign-in with the same external_id
    THEN it returns 200 OK with the users details
    """
    # create an active user in the database
    external_id = "auth|active-user-123"
    active_user = User(external_id=external_id)
    async_db_session.add(active_user)
    async_db_session.flush()
    async_db_session.refresh(active_user)
    async_db_session.commit()
    # makes a request to sign in
    headers = {"X-External-User-ID": external_id}
    response = await async_client.post(url="/users-api/sign-in", headers=headers)
    # check for a successful response and correct data
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(active_user.id)
    assert data["external_id"] == external_id


async def test_sign_in_user_is_not_found_if_external_id_does_not_exist(
    async_client: AsyncClient
):
    """
    GIVEN an active user exists in the database
    WHEN a POST request is made to /sign-in with the same external_id
    THEN it returns 200 OK with the users details
    """
    # create an active user in the database
    external_id = "auth|active-user-123"
    # makes a request to sign in
    headers = {"X-External-User-ID": external_id}
    response = await async_client.post(url="/users-api/sign-in", headers=headers)
    # check for a successful response and correct data
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "User not found. Please create an account first."
    }


async def test_sign_in_user_unauthorized_missing_header(async_client: AsyncClient):
    """
    GIVEN no authentication header is provided
    WHEN a POST request is made to /sign-in
    THEN it returns 401 Unauthorized
    """
    # make a request with no headers
    response = await async_client.post(url="/users-api/sign-in")
    # check for the 401 error from the security dependency
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Missing X-External-User-ID header"}


# DELETE USER


async def test_delete_user_success(async_client: AsyncClient, async_db_session: AsyncSession):
    """
    GIVEN a user exists in the database
    AND a request to delete a user_id with a matching external_id
    WHEN the DELETE request is made
    THEN it returns 204
    """
    # create a user in the database to get a valid user_id
    external_id = "auth|user_to_delete_123"
    test_user = User(external_id=external_id)
    async_db_session.add(test_user)
    async_db_session.flush()
    async_db_session.refresh(test_user)
    async_db_session.commit()
    # craft the request
    user_id_to_delete = test_user.id
    headers = {"X-External-User-ID": "auth|user_to_delete_123"}
    # make the authorized DELETE request.
    response = await async_client.delete(
        url=f"/users-api/users/{user_id_to_delete}", headers=headers
    )
    # check for a successful response and confirm deletion.
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # verify the user is no longer in the database.
    user_in_db = await async_db_session.get(User, user_id_to_delete)
    assert user_in_db is None


async def test_delete_user_not_found(async_client: AsyncClient):
    """
    GIVEN a user does not exist in the database
    AND a request to delete a user_id with an external_id
    WHEN the DELETE request is made
    THEN it returns 404
    """
    external_id = "auth|user_to_delete_123"
    user_id_to_delete = uuid.uuid4()
    # craft the request
    headers = {"X-External-User-ID": "auth|user_to_delete_123"}
    # make the authorized DELETE request.
    response = await async_client.delete(
        url=f"/users-api/users/{user_id_to_delete}", headers=headers
    )
    # check for a 404 response.
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # check the detail message for clarity.
    assert response.json()["detail"] == f"User with id '{user_id_to_delete}' not found."


async def test_delete_user_forbidden(async_client: AsyncClient, async_db_session: AsyncSession):
    """
    GIVEN a user A does exist in the database
    AND a user B does exist in the database
    WHEN B requests to DELETE A
    THEN it returns 403
    """
    # create user A
    user_a = User(external_id="auth|user_to_delete_123")
    async_db_session.add(user_a)
    await async_db_session.flush()
    await async_db_session.refresh(user_a)
    await async_db_session.commit()
    # create user B
    user_b = User(external_id="auth|user_to_keep_456")
    async_db_session.add(user_b)
    await async_db_session.flush()
    await async_db_session.refresh(user_b)
    await async_db_session.commit()
    # craft the request
    headers = {"X-External-User-ID": "auth|user_to_keep_456"}
    # make the authorized DELETE request.
    response = await async_client.delete(url=f"/users-api/users/{user_a.id}", headers=headers)
    # check for a 404 response.
    assert response.status_code == status.HTTP_403_FORBIDDEN
    # check the detail message for clarity.
    assert (
        response.json()["detail"] == "You do not have permission to delete this user."
    )
    # verify the users are not deleted from the database.
    user_in_db = await async_db_session.get(User, user_a.id)
    assert user_in_db is not None
    assert user_in_db.external_id == "auth|user_to_delete_123"
    user_in_db = await async_db_session.get(User, user_b.id)
    assert user_in_db is not None
    assert user_in_db.external_id == "auth|user_to_keep_456"
