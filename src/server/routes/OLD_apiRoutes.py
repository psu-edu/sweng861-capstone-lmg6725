import requests

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

    try:
        # Find the authenticated user.
        current_user = (
            session.query(User)
            .filter(
                User.provider_id == g.user_id
            )
            .first()
        )

        if not current_user:
            return jsonify({
                "error": "User not found"
            }), 404

        # Read the JSON request.
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

        try:
            # Try the real Drift AI service first.
            response = ask_drift(
                prompt,
                DRIFT_API_KEY
            )

            print(
                "AI response:",
                response
            )

            if not validate_response(response):
                return jsonify({
                    "error": "Invalid AI response"
                }), 400

            ai_response = (
                response["choices"][0]
                ["message"]["content"]
            )

            development_fallback = False

        except requests.exceptions.ConnectionError:
            # DEVELOPMENT FALLBACK:
            # The provided Drift server is currently
            # refusing connections. This allows the
            # rest of the scheduling integration to
            # be developed and tested.
            print(
                "Drift unavailable. "
                "Using development fallback."
            )

            # DEVELOPMENT FALLBACK:
            # The provided Drift server is currently unavailable.
            # This simple classifier allows the AI-assisted scheduling
            # workflow to be developed and tested without inventing
            # appointment availability.
            prompt_lower = prompt.lower()


            # ---------------------------------------------------------
            # Determine service category from words in the user's request
            # ---------------------------------------------------------

            if any(
                word in prompt_lower
                for word in [
                    "vaccine",
                    "vaccination",
                    "flu shot",
                    "shot",
                    "immunization"
                ]
            ):
                fallback_service = "Vaccination"

            elif any(
                word in prompt_lower
                for word in [
                    "sports",
                    "sport",
                    "knee",
                    "ankle",
                    "shoulder",
                    "wrist",
                    "sprain",
                    "injury",
                    "injured"
                ]
            ):
                fallback_service = "Sports Injury"

            elif any(
                word in prompt_lower
                for word in [
                    "wellness",
                    "checkup",
                    "check up",
                    "physical",
                    "routine"
                ]
            ):
                fallback_service = "Wellness Visit"

            else:
                # Use General Visit when the request does not clearly
                # match one of the more specific scheduling categories.
                fallback_service = "General Visit"


            # ---------------------------------------------------------
            # Determine preferred time from words in the user's request
            # ---------------------------------------------------------

            if any(
                phrase in prompt_lower
                for phrase in [
                    "morning",
                    "before noon",
                    "before lunch",
                    "early"
                ]
            ):
                fallback_time = "morning"

            elif any(
                phrase in prompt_lower
                for phrase in [
                    "afternoon",
                    "after noon",
                    "after lunch",
                    "later in the day"
                ]
            ):
                fallback_time = "afternoon"

            else:
                # No scheduling preference was detected.
                fallback_time = "any"


            # Format the fallback exactly like the response we expect
            # from the real scheduling assistant.
            ai_response = (
                f"SERVICE_CATEGORY: {fallback_service}\n"
                f"TIME_PREFERENCE: {fallback_time}"
            )


            response = {
                "development_fallback": True,
                "choices": [
                    {
                        "message": {
                            "content": ai_response
                        }
                    }
                ]
            }

            development_fallback = True

            print(
                "Development fallback classification:",
                ai_response
            )

            response = {
                "development_fallback": True,
                "choices": [
                    {
                        "message": {
                            "content": ai_response
                        }
                    }
                ]
            }

            development_fallback = True

        # Store the prompt and AI/fallback response.
        prompt_record = Prompt(
            prompt=prompt,
            response=ai_response,
            user_id=current_user.id
        )

        session.add(prompt_record)
        session.commit()

        return jsonify({
            "choices": response["choices"],
            "development_fallback":
                development_fallback
        }), 200

    except Exception as e:
        import traceback

        session.rollback()

        print(
            "ASK AI ERROR:",
            str(e)
        )

        traceback.print_exc()

        return jsonify({
            "error":
                "An error occurred while "
                "processing your request"
        }), 500

    finally:
        session.close()