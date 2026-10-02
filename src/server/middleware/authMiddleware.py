from flask import Blueprint, jsonify, request, g, session
from functools import wraps
import jwt
from models.database import SessionLocal
from models import User

# Authentication Middleware
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        if "access_token" in session:
            g.user_id = session.get("user_id")
            g.email = session.get("email")
            g.name = session.get("name")
            return f(*args, **kwargs)


        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "error": "Unauthorized",
                "message": "Valid access token is required"
            }), 401

        auth_returned = auth_header.split()

        if len(auth_returned) != 2 or auth_returned[0].lower() != "bearer":
            return jsonify({
                "error": "Unauthorized",
                "message": "Invalid authorization header"
            }), 401

        access_token = auth_returned[1]

        """# Verify token matches logged-in session
        if access_token != session.get("access_token"):
            return jsonify({
                "error": "Unauthorized",
                "message": "Valid access token is required"
            }), 401

        g.user_id = session.get("user_id")
        g.email = session.get("email")
        g.name = session.get("name")"""

        try:
            # Decode the token payload to identify the authenticated user.
            payload = jwt.decode(
                access_token,
                options={"verify_signature": False}
            )

            email = payload.get("sub")

            db = SessionLocal()

            user = (
                db.query(User)
                .filter(User.email == email)
                .first()
            )

            if not user:
                db.close()

                return jsonify({
                    "error": "Unauthorized",
                    "message": "User not found"
                }), 401

            g.user_id = user.provider_id
            g.email = user.email
            g.name = user.name

            db.close()

        except Exception:
            return jsonify({
                "error": "Unauthorized",
                "message": "Invalid token"
            }), 401
      

        return f(*args, **kwargs)

    return decorated