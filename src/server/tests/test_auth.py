# Test the authentication routes

def test_register(client):
    response = client.post(
        "/register",
        json={
            "email": "test@test.com",
            "username": "tester",
            "name": "Test User",
            "password": "Password123"
        }
    )

    assert response.status_code in [201, 409]


def test_session_info_logged_out(client):
    """A logged-out browser can query session state without crashing."""
    response = client.get("/session-info")

    assert response.status_code == 200

    data = response.get_json()
    assert data["logged_in"] is False
    assert data.get("role") is None


def test_logout(client):
    response = client.get("/logout")
    assert response.status_code in [200, 302]
