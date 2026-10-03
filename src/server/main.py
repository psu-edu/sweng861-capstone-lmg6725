from flask import (
    Flask,
    jsonify,
    session,
    send_from_directory,
    request,
    g,
    redirect
)
from functools import wraps
from datetime import datetime, timezone
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import logging
from authlib.integrations.flask_client import OAuth
import models
from models.database import engine, SessionLocal
from config import (
    SECRET_KEY,
    OKTA_CLIENT_ID,
    OKTA_CLIENT_SECRET,
    OKTA_ISSUER,
    OKTA_REDIRECT_URL
)
from models import Base
from User import User
from models.prompt import Prompt
# for logging
import time
import uuid
from logging_config import configure_logging

# for metrics
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from metrics import REQUEST_COUNT, REQUEST_LATENCY

# import extensions
from extensions import oauth, limiter

# import routes
from middleware.authMiddleware import require_auth
from routes.authRoutes import auth_bp
from routes.userRoutes import user_bp
from routes.healthRoutes import health_bp
from routes.apiRoutes import api_bp
from routes.aiPromptsRoutes import prompt_bp
from routes.appointmentRoutes import appointment_bp

# Initialize Flask application
app = Flask(__name__)
app.config.update(
    SECRET_KEY = SECRET_KEY,
    SESSION_COOKIE_SAMESITE = "Lax",
    SESSION_COOKIE_SECURE = False,
    SESSION_COOKIE_HTTPONLY = True,
    SESSION_COOKIE_NAME = "sweng861_session"
)
CORS(
    app,
    supports_credentials=True,
    origins=["http://localhost:5173"]
)
# import logging from app folder
logger = configure_logging()
# Initialize extensions after Flask session configuration is set.
oauth.init_app(app)
limiter.init_app(app)

# Register blueprints for different routes
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(health_bp)
app.register_blueprint(api_bp)
app.register_blueprint(prompt_bp)
app.register_blueprint(appointment_bp)
Base.metadata.create_all(bind=engine) # create tables if they don't exist

# Register the Okta OAuth client with the necessary configuration
oauth.register( 
    name="okta",
    client_id=OKTA_CLIENT_ID,
    client_secret=OKTA_CLIENT_SECRET,
    server_metadata_url=f"{OKTA_ISSUER}/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid profile email"
        }
)

# Home page
@app.route("/")
def home():
    return send_from_directory("../client", "index.html")

@app.route("/test-session")
def test_session():
    session["test"] = "hello"
    return str(session)

# Set up logging
#logging.basicConfig(filename="security.log", level=logging.INFO)

@app.before_request
def start_request():
    g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    g.start_time = time.perf_counter()

@app.after_request
def log_request(response):
    duration = time.perf_counter() - g.start_time

    REQUEST_COUNT.labels(
        method=request.method,
        path=request.path,
        status=response.status_code
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        path=request.path
    ).observe(duration)

    logger.info(
        "request_completed",
        extra={
            "request_id": getattr(g, "request_id", None),
            "method": request.method,
            "path": request.path,
            "status_code": response.status_code,
        }
    )

    response.headers["X-Request-ID"] = getattr(
        g,
        "request_id",
        ""
    )

    return response

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
    #app.run(debug=True)

