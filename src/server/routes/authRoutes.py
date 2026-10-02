from datetime import datetime, timezone
from flask import Blueprint, jsonify, redirect, request, session
from config import OKTA_REDIRECT_URL
from models.database import SessionLocal
from User import User
from extensions import limiter, oauth
from passlib.hash import bcrypt
import os

# Blueprint for all authentication-related API endpoints
auth_bp = Blueprint("auth", __name__)

# Get URL
FRONTEND_URL = os.getenv("FRONTEND_URL")

# Login
@auth_bp.route("/login", methods=["GET"])
@limiter.limit("10 per minute") # Limit for this route
def login():
    print("Login route accessed")
    print("session before callback:", dict(session))
    print("session id before callback:", session)

    try:
        response = oauth.okta.authorize_redirect(
            redirect_uri=OKTA_REDIRECT_URL
        )
        print("session after redirect:", dict(session))
        print("login response cookies:", response.headers.get("Set-Cookie"))
        return response

    except Exception as e:
        import traceback

        print("LOGIN ERROR:")
        traceback.print_exc()

        return jsonify({
            "error": str(e)
        }), 500

# test that the register route works
@auth_bp.route("/register-test", methods=["GET"])
def register_test():
    return "Register route works"

# Register a new user
@auth_bp.route("/register", methods=["POST"])
def register():
    session = SessionLocal()
    try:
        print("Content-Type:", request.content_type)
        print("Raw Data:", request.data)

        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        name = data.get("name")
        username = data.get("username")

        if not email or not password:
            return jsonify({
                "error": "Email and password are required"
                }), 400
        # Check if the user already exists in the database
        existing_user = session.query(User).filter(
            User.email == email
            ).first()   
        # If the user already exists, return a conflict error
        if existing_user:
            return jsonify({
                "error": "User already exists"
                }), 409
        # Create a new user and add to the database
        user = User(
            email = email,
            name = name,
            username = username,
            password_hash=bcrypt.hash(password),
            role="patient",
            created_at=datetime.now(timezone.utc),
            last_login=datetime.now(timezone.utc)
        )
        session.add(user)
        session.commit()
        return jsonify({
            "message": "User registered successfully"
            }), 201
    except Exception as e:
        session.rollback()
        return jsonify({
            "error": str(e)
            }), 500

    finally:
        session.close()

# Logout
@auth_bp.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.clear()
    return redirect(f"{FRONTEND_URL}/login")

# Authorization callback
@auth_bp.route("/authorize/callback")
def authorize():
    try:
        print("Authorize callback route accessed")
        print("session in callback:", dict(session))
        print("session id in callback:", session)
        print("before token")
        token = oauth.okta.authorize_access_token()
        print("after token")
        userinfo = token["userinfo"]
        print("User info received")
        provider_id = userinfo["sub"]
        email = userinfo.get("email")
        name = userinfo.get("name")
        id_token = token.get("id_token")
        access_token = token.get("access_token")

        db = SessionLocal()

        user = (
        db.query(User)
        .filter(User.provider_id == provider_id)
        .first()
        )
        # Check if user exists, if not add to database
        if not user:
            user = User(
                provider_id=provider_id,
                email = email,
                name = name,
                password_hash = "oauth_user",  # No password hash for OAuth users
                role = "patient",
                created_at=datetime.now(timezone.utc),
                last_login=datetime.now(timezone.utc)
            )
            db.add(user) # Add user

        else: # Update existing user
            user.email = email
            user.name = name
            user.last_login = datetime.now(timezone.utc)

        db.commit()
        db.close()

        session["email"] = email
        session["name"] = name
        session["user_id"] = provider_id
        session["access_token"] = access_token

        if id_token and access_token:

            """return jsonify({
                "message": "Log in successful",
                "access_token": access_token})"""
            return redirect(f"{FRONTEND_URL}/dashboard")
        else:
            return jsonify({
                "message": "Log in not successful"
                })
        #return redirect(url_for("home"))
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("token error ", str(e))

        return redirect(f"{FRONTEND_URL}/login?error=true")

# Return session information
@auth_bp.route("/session-info")
def session_info():
    return jsonify({
        "logged_in": "access_token" in session,
        "access_token": session.get("access_token")
    })