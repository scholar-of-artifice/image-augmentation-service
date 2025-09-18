import uuid
from fastapi import status

def test_create_and_delete_a_user(http_client):
    """
    This test creates a user and then deletes it.
    1. A user is created successfully.
    2. The same user is deleted successfully.
    3. A final check confirms the user is truly gone.
    """
    external_id = str(uuid.uuid4())
    headers = {"X-External-User-ID": external_id}
    # --- CREATE A USER ---
    create_user_response = http_client.post(url=f"/users-api/users", headers=headers)
    assert create_user_response.status_code == status.HTTP_201_CREATED
    create_user_response_json = create_user_response.json()
    # --- DELETE A USER ---
    user_id = create_user_response_json["id"]
    delete_response = http_client.delete(url=f"/users-api/users/{user_id}", headers=headers)
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    # --- CHECK THE USER IS FULLY GONE ---
    verify_response = http_client.post(url=f"/users-api/sign-in", headers=headers)
    assert verify_response.status_code == status.HTTP_404_NOT_FOUND

