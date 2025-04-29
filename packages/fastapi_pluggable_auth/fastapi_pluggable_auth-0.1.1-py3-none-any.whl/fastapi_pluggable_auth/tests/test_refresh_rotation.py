# fastapi_pluggable_auth/tests/test_refresh_rotation.py
import pytest
from fastapi_pluggable_auth.models import User
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_refresh_rotation(client: AsyncClient, GOOD_PW: str):
    # Create & verify user
    email = "r@x.com"
    signup_response = await client.post(
        "/auth/signup", json={"email": email, "password": GOOD_PW}
    )
    assert (
        signup_response.status_code == 201
    ), f"Signup failed: {signup_response.json()}"
    signup_data = signup_response.json()
    assert (
        signup_data["email"] == email.lower()
    ), f"Expected email {email}, got {signup_data['email']}"

    # Verify user exists in database
    user = await User.get_or_none(email=email.lower())
    assert user is not None, f"User with email {email} not found in database"
    user.is_verified = True
    await user.save()

    # Login -> pair1
    login_response = await client.post(
        "/auth/login", json={"email": email, "password": GOOD_PW}
    )
    assert login_response.status_code == 200, f"Login failed: {login_response.json()}"
    pair1 = login_response.json()

    # Refresh -> pair2
    refresh_response = await client.post(
        "/auth/refresh", json={"token": pair1["refresh_token"]}
    )
    assert (
        refresh_response.status_code == 200
    ), f"Refresh failed: {refresh_response.json()}"
    pair2 = refresh_response.json()

    # Old refresh token now invalid
    retry_refresh_response = await client.post(
        "/auth/refresh", json={"token": pair1["refresh_token"]}
    )
    assert (
        retry_refresh_response.status_code == 401
    ), f"Expected 401 for old refresh token: {retry_refresh_response.json()}"

    # Logout -> all tokens dead
    headers = {"Authorization": f"Bearer {pair2['access_token']}"}
    logout_response = await client.post("/auth/logout", headers=headers)
    assert (
        logout_response.status_code == 200
    ), f"Logout failed: {logout_response.json()}"

    # Verify refresh token is invalid after logout
    final_refresh_response = await client.post(
        "/auth/refresh", json={"token": pair2["refresh_token"]}
    )
    assert (
        final_refresh_response.status_code == 401
    ), f"Expected 401 after logout: {final_refresh_response.json()}"
