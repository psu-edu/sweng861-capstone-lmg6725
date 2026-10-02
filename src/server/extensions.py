# app/extensions.py

# Shared extensions for the Flask application

# Enable authentication via third party providers
from authlib.integrations.flask_client import OAuth

# Enable rate limiting request throttling to reduce abuse and protect API endpoints
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
oauth = OAuth()

# Rate limit is tracked by client IP address
limiter = Limiter(
key_func=get_remote_address,

)