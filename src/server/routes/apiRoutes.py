from flask import Blueprint, request, jsonify
from services.drift_client import ask_drift
from services.drift_validator import validate_response
from config import DRIFT_API_KEY
from models.prompt import Prompt
from models.database import SessionLocal
from flask import g
from User import User
from middleware.authMiddleware import require_auth

api_bp = Blueprint("api", __name__)

@api_bp.route("/ask-ai", methods=["POST"])
@require_auth
def ask_ai():
    print("ASK AI ROUTE HIT")
    session = SessionLocal()

    current_user = (
        session.query(User)
        .filter(User.provider_id == g.user_id)
        .first()
    )

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Missing JSON body"
        }), 400

    if "prompt" not in data:
        return jsonify({
            "error": "Prompt required"
        }), 400


    prompt = data["prompt"]
    print("calling drift")
    print("DRIFT KEY:", DRIFT_API_KEY)
    response = ask_drift(prompt, DRIFT_API_KEY)
    print(response.status_code)
    print(response.text)

    if not validate_response(response):
        return jsonify({
            "error": "Invalid AI response"
        }), 400

    # Store response in the database
    ai_response = response["choices"][0]["message"]["content"]
    # Format prompt to store in database
    prompt_record = Prompt(
        prompt=prompt,
        response=ai_response,
        user_id=current_user.id
    )
    # Add prompt to database
    session.add(prompt_record)
    session.commit()

    return jsonify(response)