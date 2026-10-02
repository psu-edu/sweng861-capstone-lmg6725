from flask import request, jsonify, g, redirect, session
from flask import Blueprint
from middleware.authMiddleware import require_auth
import logging
from models.database import SessionLocal
from User import User
from flask import g


# Set up logging
logging.basicConfig(filename="security.log", level=logging.INFO)

user_bp = Blueprint("user", __name__)

# Protected Endpoint
# To use must pass in bearer token (can not be used without it)
@user_bp.route('/api/hello')
@require_auth
def hello():
    logging.info(f"Accessing protected endpoint")
    return jsonify(
        {
            "message": f"Hello, {g.email}!"
        })

# Return user profile information
@user_bp.route("/profile")
@require_auth
def profile():
    return jsonify({
        "user_id": g.user_id,
        "email": g.email
    })

# Return user information for the authenticated user
@user_bp.route("/users/me")
@require_auth
def get_users():
    db = SessionLocal()
    user = (
        db.query(User)
        .filter(User.provider_id == g.user_id)
        .first()
    )
    if not user:
        db.close()
        return "User not found", 404

    result = {
            "email": user.email, 
            "name": user.name,
            "created_at": user.created_at,
            "last_login": user.last_login}
    
    db.close()
    return jsonify(result)

# Check if a user is an admin
@user_bp.route("/users", methods=["GET"])
@require_auth
def get_all_users():

    session = SessionLocal()
    try:
        current_user = (
            session.query(User)
            .filter(User.provider_id == g.user_id)
            .first()
        )

        if current_user.role != "admin":
            return jsonify({
                "error": "Admin access required"
            }), 403

        if current_user.role == "admin":
            session = SessionLocal()
            users = session.query(User).all()
            return jsonify([
                {
                    "id": u.id,
                    "provider_id": u.provider_id,
                    "email": u.email,
                    "name": u.name,
                    "username": u.username,
                    "role": u.role,
                    "created_at": u.created_at,
                    "last_login": u.last_login
                }
                for u in users
            ])
    finally:
        session.close()

# Return a greeting and the authenticated user's name 
# A check to verify we are authenticated and returning data
@user_bp.route("/protected")
@require_auth
def protected():
    return jsonify({
        "message": f"Hello, {g.name or 'user'}!",
        "name": g.name
    })
