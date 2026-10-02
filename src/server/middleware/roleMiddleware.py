from functools import wraps
from flask import jsonify, g
from models.database import SessionLocal
from User import User

def require_role(*roles):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            db = SessionLocal()

            user = (
                db.query(User)
                .filter(User.provider_id == g.user_id)
                .first()
            )

            db.close()

            if not user:
                return jsonify({
                    "error": "User not found"
                }), 404

            if user.role not in roles:
                return jsonify({
                    "error": "Access denied"
                }), 403

            return f(*args, **kwargs)

        return wrapped
    return decorator