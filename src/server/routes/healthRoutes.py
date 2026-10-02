from flask import Blueprint, jsonify, session
from sqlalchemy import text
from models.database import engine

health_bp = Blueprint("health", __name__)


# Health check
@health_bp.route("/health", methods=["GET"])
def health():
    try:
        # check connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        # successful 200
        return jsonify({
            "status": "UP",
            "db": "UP"
        }), 200
    
    # can't be reached 503
    except Exception:
        return jsonify({
            "status": "DOWN",
            "db": "DOWN"
        }), 503

# Debug session
"""@health_bp.route("/debug-session")
def debug_session():
    return jsonify(dict(session))"""

# Liveness check (verify app can respond)
@health_bp.route("/health/live", methods=["GET"])
def health_live():
    return jsonify({
    "status": "UP"
    }), 200

# Readiness check (check can access database)
@health_bp.route("/health/ready", methods=["GET"])
def health_ready():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return jsonify({
            "status": "READY",
            "db": "UP"
        }), 200
    
    except Exception:
        return jsonify({
            "status": "NOT_READY",
            "db": "DOWN"
        }), 503