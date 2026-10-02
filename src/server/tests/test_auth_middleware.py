from flask import Flask
from middleware.authMiddleware import require_auth

def create_app():

    app = Flask(__name__)

    @app.route("/protected")
    @require_auth
    def protected():
        return {"success": True}

    return app

def test_missing_header_returns_401():

    app = create_app()

    client = app.test_client()

    response = client.get("/protected")

    assert response.status_code == 401

def test_invalid_header_returns_401():

    app = create_app()

    client = app.test_client()

    response = client.get(
        "/protected",
        headers={
            "Authorization": "BadHeader"
        }
    )

    assert response.status_code == 401

def test_invalid_token_returns_401(mocker):

    app = create_app()

    client = app.test_client()

    mocker.patch(
        "middleware.authMiddleware.jwt.decode",
        side_effect=Exception()
    )

    response = client.get(
        "/protected",
        headers={
            "Authorization": "Bearer fake"
        }
    )

    assert response.status_code == 401
